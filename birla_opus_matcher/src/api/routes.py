from __future__ import annotations

from flask import Blueprint, request, jsonify

from src.core.image_processing import decode_image, extract_dominant_rgb, InvalidImageError
from src.core.matcher import BirlaOpusMatcher


def create_routes(matcher: BirlaOpusMatcher) -> Blueprint:
    bp = Blueprint("api", __name__)

    @bp.get("/health")
    def health():
        return jsonify({"status": "ok", "shades_loaded": len(matcher.db.shades)}), 200

    @bp.post("/match")
    def match_shade():
        """
        POST form-data:
          image=<file>
        Optional query:
          ?k=5  (top results)
        """
        k = request.args.get("k", default="5")

        if "image" not in request.files:
            return jsonify({"error": "Missing file field 'image'."}), 400

        f = request.files["image"]
        if not f or f.filename.strip() == "":
            return jsonify({"error": "No file uploaded."}), 400

        try:
            img = decode_image(f.read())
            rgb = extract_dominant_rgb(img)

            result = matcher.match_rgb(rgb, top_k=int(k))
            return jsonify(result), 200

        except ValueError:
            return jsonify({"error": "Invalid query parameter 'k'. Must be integer."}), 400

        except InvalidImageError as e:
            return jsonify({"error": str(e)}), 400

        except Exception:
            return jsonify({"error": "Internal server error."}), 500

    @bp.post("/match_rgb")
    def match_rgb():
        """
        POST JSON:
        {
          "r": 238,
          "g": 224,
          "b": 139,
          "k": 5
        }
        """
        data = request.get_json(silent=True) or {}
        try:
            r = int(data["r"])
            g = int(data["g"])
            b = int(data["b"])
            k = int(data.get("k", 5))
        except Exception:
            return jsonify({"error": "Invalid JSON. Required keys: r,g,b. Optional: k"}), 400

        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            return jsonify({"error": "RGB values must be between 0 and 255."}), 400

        result = matcher.match_rgb((r, g, b), top_k=k)
        return jsonify(result), 200

    return bp
