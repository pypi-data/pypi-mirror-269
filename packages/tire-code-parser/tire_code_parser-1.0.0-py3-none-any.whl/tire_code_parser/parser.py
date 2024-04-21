import re


def parse_tire_code(tire_code: str) -> dict[str, str]:
    pattern: re.Pattern = re.compile(
        r"(P|LT|ST|T|)(\d{3})(?:\/?(\d{2,3}|)\/?\s?(B|D|R|)(\d{1,2}|)(?:LR|)?([A-N]|)?)?"
    )
    matches: re.Match[str] | None = pattern.match(tire_code)

    if not matches:
        raise ValueError("Invalid tire code format")

    matches_groups: tuple[str, ...] = matches.groups()
    (
        vehicle_class,
        section_width_mm,
        aspect_ratio,
        construction,
        wheel_diameter_in,
        load_range,
    ) = matches_groups

    vehicle_class_mapping = {
        "P": "Passenger Car",
        "LT": "Light Truck",
        "ST": "Special Trailer",
        "T": "Temporary",
        "": "",
    }
    vehicle_class: str = vehicle_class_mapping[vehicle_class]

    section_width_in: str = str(round(float(section_width_mm) / 25.4, 1))

    if aspect_ratio:
        aspect_ratio: str = str(float(aspect_ratio) / 100)

    load_range_mapping = {
        "B": "Bias belt",
        "D": "Diagonal",
        "R": "Radial",
        "": "Cross-ply",
    }
    construction_translated = load_range_mapping[construction]

    load_range_to_ply_mapping = {
        "A": "2",
        "B": "4",
        "C": "6",
        "D": "8",
        "E": "10",
        "F": "12",
        "G": "14",
        "H": "16",
        "J": "18",
        "L": "20",
        "M": "22",
        "N": "24",
        "": "",
    }
    ply_rating: str = load_range_to_ply_mapping[load_range]

    if wheel_diameter_in:
        tire_diameter_in: str = str(
            round(
                (
                    float(wheel_diameter_in)
                    + 2 * (float(section_width_in) * float(aspect_ratio))
                ),
                1,
            )
        )
    else:
        tire_diameter_in = ""

    return {
        "tire_code": tire_code,
        "vehicle_class": vehicle_class,
        "section_width_mm": section_width_mm,
        "section_width_in": section_width_in,
        "aspect_ratio": aspect_ratio,
        "construction": construction_translated,
        "wheel_diameter_in": wheel_diameter_in,
        "tire_diameter_in": tire_diameter_in,
        "load_range": load_range,
        "ply_rating": ply_rating,
    }

