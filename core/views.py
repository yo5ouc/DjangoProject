import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# 📡 1. Global state dictionary tracking your active telemetry
LIVE_RIG_STATE = {
    "current_frequency": "03.573.00",
    "current_band": "80 Meters",
    "repeater_shift": "Simplex",
    "is_transmitting": False,
    "smeter": 0,
    "tx_power": 0,
    "alc": 0,
    "pending_command": ""
}


# -----------------------------------------------------------------
# 📻 2. RADIO TRANSLATION DRIVER CLASSES (OOP Blueprints)
# -----------------------------------------------------------------
class BaseRadio:
    def parse_frequency(self, raw_data):
        raise NotImplementedError


class FT857D(BaseRadio):
    def parse_frequency(self, hex_data):
        try:
            # Cleanly handle the 10-digit telemetry stream from the script
            if len(hex_data) >= 10:
                clean_digits = hex_data[:-2]  # Strips the trailing '02' mode opcode
            else:
                clean_digits = hex_data[0:8]

            freq_mhz = float(clean_digits) / 1000000
            mhz_str = f"{freq_mhz:08.5f}"  # Standardizes the width (e.g. "03.57300")

            # Position slicing maps the segment dots exactly to the faceplate grid template
            whole = mhz_str[0:2]
            thousands = mhz_str[3:6]
            hundreds = mhz_str[6:8]

            return f"{whole}.{thousands}.{hundreds}"
        except (ValueError, IndexError):
            return "03.573.00"


class FT991A(BaseRadio):
    def parse_frequency(self, ascii_str):
        try:
            freq_hz = ascii_str[2:-1]
            freq_mhz = float(freq_hz) / 1000000

            mhz_str = f"{freq_mhz:08.5f}"
            whole = mhz_str[0:2]
            thousands = mhz_str[3:6]
            hundreds = mhz_str[6:8]

            return f"{whole}.{thousands}.{hundreds}"
        except (ValueError, IndexError):
            return "03.573.00"


# -----------------------------------------------------------------
# 🎛️ 3. DJANGO ROUTING API VIEWS
# -----------------------------------------------------------------
def radio_dashboard(request):
    """Renders the main web page layout template console."""
    iaru_bands = [
        {"name": "80 Meters", "freq_display": "3.573 MHz", "hex": "0035730001"},
        {"name": "40 Meters", "freq_display": "7.074 MHz", "hex": "0070740001"},
        {"name": "20 Meters", "freq_display": "14.074 MHz", "hex": "0140740001"},
        {"name": "15 Meters", "freq_display": "21.074 MHz", "hex": "0210740001"},
        {"name": "10 Meters", "freq_display": "28.074 MHz", "hex": "0280740001"},
        {"name": "6 Meters", "freq_display": "50.313 MHz", "hex": "0503130001"},
        {"name": "2 Meters", "freq_display": "144.200 MHz", "hex": "1442000001"},
        {"name": "70 Centimeters", "freq_display": "432.200 MHz", "hex": "4322000001"},
    ]
    return render(request, 'radio_dashboard.html', {'bands': iaru_bands, 'state': LIVE_RIG_STATE})


@csrf_exempt
def update_telemetry_api(request):
    """📥 Multi-rig interpretation engine endpoint."""
    global LIVE_RIG_STATE
    if request.method == "POST":
        data = json.loads(request.body)
        rig_type = data.get("rig_type", "FT-857D")
        raw_data = data.get("raw_cat", "")

        if rig_type == "FT-857D":
            driver = FT857D()
        else:
            driver = FT991A()

        # Update the values safely
        LIVE_RIG_STATE["current_frequency"] = driver.parse_frequency(raw_data)

        script_tx = data.get("tx_status", False)
        web_tx = data.get("force_tx", False)
        LIVE_RIG_STATE["is_transmitting"] = script_tx or web_tx

        LIVE_RIG_STATE["smeter"] = data.get("smeter", 0)
        LIVE_RIG_STATE["tx_power"] = data.get("tx_power", 0)
        LIVE_RIG_STATE["alc"] = data.get("alc", 0)

        response_data = {
            "status": "success",
            "pending_hardware_command": LIVE_RIG_STATE["pending_command"],
            "force_tx": LIVE_RIG_STATE["is_transmitting"]
        }

        return JsonResponse(response_data)
    return JsonResponse({"error": "Invalid method"}, status=400)


@csrf_exempt
def select_band_api(request):
    global LIVE_RIG_STATE
    if request.method == "POST":
        data = json.loads(request.body)
        LIVE_RIG_STATE["pending_command"] = data.get("hex_code")

        # ✅ FIXED: Standard float parsing rule blocks any zfill/ljust formatting errors
        raw_display = data.get("freq_display", "3.573")
        try:
            val = float(raw_display.replace(" MHz", ""))
            mhz_str = f"{val:08.5f}"
            whole = mhz_str[0:2]
            thousands = mhz_str[3:6]
            hundreds = mhz_str[6:8]
            LIVE_RIG_STATE["current_frequency"] = f"{whole}.{thousands}.{hundreds}"
        except ValueError:
            LIVE_RIG_STATE["current_frequency"] = "03.573.00"

        LIVE_RIG_STATE["current_band"] = data.get("band_name")
        return JsonResponse({"status": "staged"})
    return JsonResponse({"error": "Invalid method"}, status=400)


@csrf_exempt
def select_shift_api(request):
    global LIVE_RIG_STATE
    if request.method == "POST":
        data = json.loads(request.body)
        LIVE_RIG_STATE["pending_command"] = data.get("hex_code")
        LIVE_RIG_STATE["repeater_shift"] = data.get("shift_mode")
        return JsonResponse({"status": "staged", "mode": LIVE_RIG_STATE["repeater_shift"]})
    return JsonResponse({"error": "Invalid method"}, status=400)


@csrf_exempt
def get_status_api(request):
    return JsonResponse(LIVE_RIG_STATE)
