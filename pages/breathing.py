from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.clock import Clock
from functions.alcohol import measure_alcohol, stop_measurement
from functions.camera import take_snapshot
import os
from datetime import datetime


class Breathing(MDScreen):

    _measurement_active = False

    def on_enter(self):
        print("Start alcohol test...")
        self._measurement_active = True
        # Reset UI state
        self._update_status_label("กำลังเชื่อมต่ออุปกรณ์... / Connecting...")
        self._set_icon_color("blue")
        self._hide_error_box()
        # Start real measurement
        measure_alcohol(self._on_device_status, self._on_measurement_result)

    def on_leave(self):
        """Clean up if user navigates away mid-measurement."""
        if self._measurement_active:
            stop_measurement()
            self._measurement_active = False

    # ── Status callback (called from Kivy main thread) ────────
    def _on_device_status(self, state, message):
        """Update UI to reflect current device state."""
        if not self._measurement_active:
            return

        print(f"[breathing] status: {state} -> {message}")
        self._update_status_label(message)

        # Update icon colour by state
        color_map = {
            "connecting":      "gray",
            "warming_up":      "orange",
            "ready":           "green",
            "breath_detected": "green",
            "sampling":        "orange",
            "analyzing":       "orange",
            "flow_error":      "red",
            "timeout":         "red",
            "error":           "red",
        }
        self._set_icon_color(color_map.get(state, "blue"))

        # Show error box for terminal error states
        if state in ("timeout", "error"):
            self._show_error_box(message)

    # ── Result callback (called from Kivy main thread) ────────
    def _on_measurement_result(self, success, value, status):
        """Handle final measurement result."""
        self._measurement_active = False
        print(f"[breathing] result: success={success}, value={value}, status={status}")

        app = MDApp.get_running_app()

        if success:
            # Save to session
            app.session.alcohol_value = value
            app.session.alcohol_status = status
            self._update_status_label(
                f"ผลตรวจ: {value} ({status}) / Result: {value} ({status})"
            )
            self._set_icon_color("green")

            # Take snapshot then navigate
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            snapshot_path = os.path.join(
                os.getcwd(), "assets", "snapshots", f"breathing_{timestamp}.jpg"
            )
            app.session.snapshot_path = snapshot_path
            take_snapshot(snapshot_path, self._on_snapshot_done)
        else:
            # Save error state to session
            app.session.alcohol_value = -1.0
            app.session.alcohol_status = status  # NO_PORT / TIMEOUT / ERROR etc.
            self._show_error_box(
                f"การวัดล้มเหลว ({status}) / Measurement failed ({status})"
            )

    # ── Snapshot callback ─────────────────────────────────────
    def _on_snapshot_done(self, success, path):
        if success:
            print(f"Snapshot saved: {path}")
        else:
            print("Snapshot failed or camera unavailable.")
            MDApp.get_running_app().session.snapshot_path = ""
        self._navigate_to_result()

    # ── Retry / Cancel ────────────────────────────────────────
    def retry_measurement(self):
        """User pressed Retry — restart the measurement cycle."""
        print("[breathing] Retrying measurement...")
        self._hide_error_box()
        self._measurement_active = True
        self._update_status_label("กำลังเชื่อมต่ออุปกรณ์... / Connecting...")
        self._set_icon_color("blue")
        measure_alcohol(self._on_device_status, self._on_measurement_result)

    def cancel_measurement(self):
        """User pressed Cancel — go back to home."""
        print("[breathing] Measurement cancelled by user.")
        stop_measurement()
        self._measurement_active = False
        if self.manager:
            self.manager.current = "home"

    # ── Navigation ────────────────────────────────────────────
    def _navigate_to_result(self):
        if self.manager:
            self.manager.current = "testresult"

    # ── UI helpers ────────────────────────────────────────────
    def _update_status_label(self, text):
        if "status_label" in self.ids:
            self.ids.status_label.text = text

    def _set_icon_color(self, color_name):
        color_map = {
            "blue":   [0.2, 0.4, 1, 1],
            "green":  [0.2, 0.8, 0.3, 1],
            "orange": [1, 0.6, 0, 1],
            "red":    [0.9, 0.2, 0.2, 1],
            "gray":   [0.6, 0.6, 0.6, 1],
        }
        if "status_icon" in self.ids:
            self.ids.status_icon.md_bg_color = color_map.get(color_name, [0.2, 0.4, 1, 1])

    def _show_error_box(self, message):
        if "error_label" in self.ids:
            self.ids.error_label.text = message
        if "error_box" in self.ids:
            self.ids.error_box.opacity = 1
            self.ids.error_box.disabled = False

    def _hide_error_box(self):
        if "error_box" in self.ids:
            self.ids.error_box.opacity = 0
            self.ids.error_box.disabled = True