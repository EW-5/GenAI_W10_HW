"""Run a local, headless Edge smoke test over every slide at three sizes."""
from contextlib import closing
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from pathlib import Path
import json
import os
import subprocess
from tempfile import TemporaryDirectory
from threading import Thread
from time import monotonic, sleep
from urllib.request import urlopen

import websocket

from build_wiki import ROOT

EDGE = Path(os.environ.get("EDGE_PATH",
                          r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"))


class QuietHandler(SimpleHTTPRequestHandler):
    def handle(self):
        try:
            super().handle()
        except ConnectionResetError:
            # A tab may close an idle HTTP connection during navigation.
            pass

    def log_message(self, *args):
        pass


def connect(profile):
    port_file = Path(profile) / "DevToolsActivePort"
    deadline = monotonic() + 12
    while monotonic() < deadline:
        if port_file.is_file():
            port = port_file.read_text().splitlines()[0]
            with urlopen(f"http://127.0.0.1:{port}/json/list", timeout=4) as response:
                tabs = json.load(response)
            tab = next(target for target in tabs if target["type"] == "page")
            return websocket.create_connection(tab["webSocketDebuggerUrl"], timeout=8,
                                               suppress_origin=True)
        sleep(0.1)
    raise RuntimeError("Edge did not start its debugging endpoint")


def check(socket, base):
    message_id = 0

    def call(method, **params):
        nonlocal message_id
        message_id += 1
        socket.send(json.dumps(dict(id=message_id, method=method, params=params)))
        while True:
            message = json.loads(socket.recv())
            if message.get("id") == message_id:
                if "error" in message:
                    raise RuntimeError(message["error"])
                return message.get("result", {})

    def js(expression):
        result = call("Runtime.evaluate", expression=expression, returnByValue=True)
        if "exceptionDetails" in result:
            raise RuntimeError(result["exceptionDetails"])
        return result["result"].get("value")

    def navigate(file, ready):
        call("Page.navigate", url=f"{base}/{file}")
        deadline = monotonic() + 8
        while monotonic() < deadline:
            if js(f"location.pathname.endsWith('/{file}') && Boolean({ready})"):
                return
            sleep(0.05)
        raise RuntimeError(f"page did not load: {file}")

    for width, height in [(1440, 900), (1024, 768), (390, 844)]:
        call("Emulation.setDeviceMetricsOverride", width=width, height=height,
             deviceScaleFactor=1, mobile=False)
        navigate("slides.html", "document.querySelector('section[data-slide]')")
        for number in range(1, 11):
            result = js("""(() => {
              const visible = [...document.querySelectorAll('[data-slide]:not([hidden])')];
              const number = document.querySelector('#counter').textContent.trim();
              const slide = visible[0], footer = document.querySelector('.controls');
              return {number, count: visible.length, slide: slide.dataset.slide,
                horizontal: document.documentElement.scrollWidth > innerWidth ||
                  slide.scrollWidth > slide.clientWidth + 1,
                vertical: Math.ceil(footer.getBoundingClientRect().bottom) > innerHeight};
            })()""")
            if result != dict(number=f"{number} / 10", count=1, slide=str(number),
                              horizontal=False, vertical=False):
                raise RuntimeError(f"{width}x{height} slide {number}: {result}")
            if number < 10:
                js("document.querySelector('#next').click()")
        if not js("document.querySelector('#next').disabled"):
            raise RuntimeError("Next does not stop at the last slide")
        js("document.querySelector('#prev').click()")
        if js("document.querySelector('#counter').textContent") != "9 / 10":
            raise RuntimeError("Previous button did not show slide 9")
        for key, expected in [("ArrowLeft", "8 / 10"), ("ArrowRight", "9 / 10")]:
            keycode = {"ArrowLeft": 37, "ArrowRight": 39}[key]
            for action in ("keyDown", "keyUp"):
                call("Input.dispatchKeyEvent", type=action, key=key, code=key,
                     windowsVirtualKeyCode=keycode)
            if js("document.querySelector('#counter').textContent") != expected:
                raise RuntimeError(f"{key} did not show {expected}")
        for _ in range(8):
            js("document.querySelector('#prev').click()")
        if not js("document.querySelector('#prev').disabled"):
            raise RuntimeError("Previous does not stop at the first slide")
        print(f"PASS Edge {width}x{height}: slides 1–10 fit; buttons, arrow keys and counter")

    navigate("index.html", "document.querySelector('main')")
    for file in ("wiki.html", "slides.html", "workflow.html"):
        if not js(f"document.querySelector('a[href=\"{file}\"]') !== null"):
            raise RuntimeError(f"missing entry link to {file}")
    navigate("workflow.html", "document.querySelector('main')")
    navigate("wiki.html", "document.querySelector('#concepts-rag')")
    with urlopen(base + "/slides.html", timeout=5) as response:
        if response.status != 200:
            raise RuntimeError("subpath did not return HTTP 200")
    print("PASS Edge: entry links, workflow and Wiki load under /rag-wiki/")


def main():
    handler = partial(QuietHandler, directory=ROOT.parent)
    with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server, TemporaryDirectory() as profile:
        Thread(target=server.serve_forever, daemon=True).start()
        process = subprocess.Popen(
            [str(EDGE), "--headless=new", "--disable-gpu", "--no-first-run",
             "--remote-debugging-port=0", f"--user-data-dir={profile}", "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        try:
            with closing(connect(profile)) as socket:
                check(socket, f"http://127.0.0.1:{server.server_port}/{ROOT.name}")
        finally:
            process.terminate()
            process.wait(timeout=8)
            server.shutdown()


if __name__ == "__main__":
    main()
