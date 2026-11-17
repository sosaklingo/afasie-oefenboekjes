"""Real-browser smoke tests for the four levels and communication board.

Run with Python Playwright and installed Chromium; set TEST_WEBKIT=1 to add
Safari-engine iPhone emulation, and TEST_CHROMIUM_PATH for local Chromium.
No data leaves the local HTTP server.
"""
import os
import threading
import unittest
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


WEB = Path(__file__).resolve().parents[1] / 'website' / 'dist'


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


class BrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(
            ('127.0.0.1', 0), partial(QuietHandler, directory=str(WEB)))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = 'http://127.0.0.1:' + str(cls.server.server_address[1]) + '/'
        cls.playwright = sync_playwright().start()

    @classmethod
    def tearDownClass(cls):
        cls.playwright.stop()
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def test_real_navigation_on_desktop_mobile_and_tablet(self):
        targets = [
            ('Desktop Chromium', 'chromium', {'width': 1280, 'height': 800}, False),
            ('Android-style Chromium', 'chromium', {'width': 390, 'height': 844}, True),
            ('Tablet Chromium', 'chromium', {'width': 820, 'height': 1180}, True),
        ]
        if os.environ.get('TEST_WEBKIT') == '1':
            targets.append(('iPhone WebKit', 'webkit', {'width': 390, 'height': 844}, True))

        for label, engine, viewport, touch in targets:
            with self.subTest(device=label):
                browser_type = getattr(self.playwright, engine)
                opts = {'headless': True}
                if engine == 'chromium' and os.environ.get('TEST_CHROMIUM_PATH'):
                    opts['executable_path'] = os.environ['TEST_CHROMIUM_PATH']
                browser = browser_type.launch(**opts)
                context = browser.new_context(viewport=viewport, has_touch=touch,
                                              is_mobile=touch, locale='nl-NL')
                page = context.new_page()
                errors = []
                page.on('pageerror', lambda error: errors.append(str(error)))
                try:
                    response = page.goto(self.base_url, wait_until='load')
                    self.assertEqual(response.status, 200)
                    for level in ('easy', 'medium', 'advanced', 'expert'):
                        page.locator('button[data-action="' + level + '"]').click()
                        self.assertEqual(page.locator('.exercise-card').count(), 1)
                        self.assertEqual(page.locator('[role="progressbar"]').get_attribute('aria-valuenow'), '1')
                        page.locator('button[data-action="hint"]').click()
                        self.assertTrue(page.locator('.exercise-card .hint').is_visible())
                        page.locator('button[data-action="answer"]').click()
                        self.assertIn('Voorbeeld:', page.locator('#answerArea').inner_text())
                        page.locator('button[data-action="next"]').click()
                        self.assertEqual(page.locator('[role="progressbar"]').get_attribute('aria-valuenow'), '2')
                        page.locator('button[data-action="home"]').click()

                    page.locator('button[data-action="board"]').click()
                    first_phrase = page.locator('button[data-phrase]').first
                    message = first_phrase.get_attribute('data-phrase')
                    first_phrase.click()
                    self.assertEqual(page.locator('#spokenText').inner_text(), message)
                    page.locator('button[data-boardtab="mijn"]').click()
                    page.locator('#personalPhrase').fill('Ik wil water')
                    page.locator('#personalForm button[type="submit"]').click()
                    self.assertEqual(page.locator('button[data-custom-index]').count(), 1)

                    # User phrases stay on this device after a browser reload.
                    page.reload(wait_until='load')
                    page.locator('button[data-action="board"]').click()
                    page.locator('button[data-boardtab="mijn"]').click()
                    self.assertIn('Ik wil water', page.locator('button[data-custom-index]').inner_text())

                    # Reading and high-contrast controls are reachable on all screen sizes.
                    page.locator('#biggerText').click()
                    page.locator('#contrastBtn').click()
                    self.assertEqual(page.locator('#contrastBtn').get_attribute('aria-pressed'), 'true')
                    self.assertTrue(page.locator('body.high-contrast').count() == 1)
                    self.assertLessEqual(
                        page.evaluate('document.documentElement.scrollWidth - window.innerWidth'),
                        2,
                        'Unexpected horizontal overflow on ' + label,
                    )
                    self.assertEqual(errors, [], 'Browser JavaScript errors on ' + label)
                finally:
                    context.close()
                    browser.close()


if __name__ == '__main__':
    unittest.main()
