"""Build the trilingual glossary in three formats: XLSX, JSON, CSV.

Theme: Automobile Industry.
Languages: Ukrainian (source) -> English -> German.

Run from project root:
    python3 scripts/build_glossary.py
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

HEADERS = ["ID", "Ukrainian", "English", "German", "Notes"]
THEME = "Automobile Industry"

# (Ukrainian, English, German, Notes)
ENTRIES: list[tuple[str, str, str, str]] = [
    # --- Vehicle types & body styles ---
    ("Легковий автомобіль", "Passenger car", "Personenkraftwagen", "Vehicle class; DE abbr. PKW"),
    ("Вантажний автомобіль", "Truck", "Lastkraftwagen", "Vehicle class; DE abbr. LKW"),
    ("Седан", "Sedan", "Limousine", "Body style; UK 'saloon'"),
    ("Хетчбек", "Hatchback", "Schrägheck", "Body style"),
    ("Універсал", "Estate car", "Kombi", "Body style; US 'station wagon'"),
    ("Позашляховик", "Off-road vehicle", "Geländewagen", "Body style"),
    ("Кросовер", "Crossover", "Crossover", "Body style; SUV-derived"),
    ("Купе", "Coupe", "Coupé", "Body style; two-door"),
    ("Кабріолет", "Convertible", "Cabriolet", "Body style; open top"),
    ("Пікап", "Pickup truck", "Pick-up", "Body style; open cargo bed"),
    ("Мікроавтобус", "Minivan", "Kleinbus", "Multi-purpose passenger vehicle"),
    ("Електромобіль", "Electric vehicle", "Elektrofahrzeug", "EN abbr. EV; DE 'E-Auto'"),

    # --- Engine & powertrain ---
    ("Двигун", "Engine", "Motor", "Core powertrain component"),
    ("Двигун внутрішнього згоряння", "Internal combustion engine", "Verbrennungsmotor", "EN abbr. ICE"),
    ("Бензиновий двигун", "Petrol engine", "Benzinmotor", "US 'gasoline engine'"),
    ("Дизельний двигун", "Diesel engine", "Dieselmotor", "Compression-ignition"),
    ("Гібридний силовий агрегат", "Hybrid powertrain", "Hybridantrieb", "ICE + electric motor"),
    ("Електродвигун", "Electric motor", "Elektromotor", "EV powertrain"),
    ("Турбонагнітач", "Turbocharger", "Turbolader", "Forced induction; informal: 'turbo'"),
    ("Циліндр", "Cylinder", "Zylinder", "Engine part"),
    ("Поршень", "Piston", "Kolben", "Engine part"),
    ("Колінчастий вал", "Crankshaft", "Kurbelwelle", "Engine part"),
    ("Розподільний вал", "Camshaft", "Nockenwelle", "Engine part"),
    ("Свічка запалювання", "Spark plug", "Zündkerze", "Petrol engines only"),
    ("Паливна форсунка", "Fuel injector", "Einspritzdüse", "Fuel-delivery component"),
    ("Радіатор", "Radiator", "Kühler", "Cooling system"),
    ("Об'єм двигуна", "Engine displacement", "Hubraum", "Measured in litres or cc"),

    # --- Transmission & drivetrain ---
    ("Коробка передач", "Gearbox", "Getriebe", "US 'transmission'"),
    ("Механічна коробка передач", "Manual transmission", "Schaltgetriebe", "Driver-operated"),
    ("Автоматична коробка передач", "Automatic transmission", "Automatikgetriebe", "Self-shifting"),
    ("Зчеплення", "Clutch", "Kupplung", "Manual transmissions"),
    ("Карданний вал", "Driveshaft", "Antriebswelle", "Drivetrain part"),
    ("Диференціал", "Differential", "Differential", "Drivetrain part"),
    ("Передній привід", "Front-wheel drive", "Frontantrieb", "EN abbr. FWD"),
    ("Задній привід", "Rear-wheel drive", "Heckantrieb", "EN abbr. RWD"),
    ("Повний привід", "All-wheel drive", "Allradantrieb", "EN abbr. AWD; also 4x4"),
    ("Передавальне число", "Gear ratio", "Übersetzungsverhältnis", "Drivetrain specification"),

    # --- Brakes, suspension, steering ---
    ("Гальмівна система", "Brake system", "Bremssystem", "Active safety"),
    ("Дискові гальма", "Disc brakes", "Scheibenbremsen", "Brake type"),
    ("Барабанні гальма", "Drum brakes", "Trommelbremsen", "Brake type"),
    ("Гальмівні колодки", "Brake pads", "Bremsbeläge", "Wear item"),
    ("Стоянкове гальмо", "Parking brake", "Handbremse", "Also 'handbrake'"),
    ("Підвіска", "Suspension", "Federung", "Chassis system"),
    ("Амортизатор", "Shock absorber", "Stoßdämpfer", "Suspension part"),
    ("Пружина підвіски", "Suspension spring", "Federbein", "Suspension part"),
    ("Кермо", "Steering wheel", "Lenkrad", "Driver interface"),
    ("Рульове управління", "Steering system", "Lenkung", "Vehicle system"),
    ("Підшипник", "Bearing", "Lager", "Generic mechanical part"),
    ("Розвал-сходження", "Wheel alignment", "Achsvermessung", "Service procedure"),

    # --- Electrical & electronics ---
    ("Акумуляторна батарея", "Battery", "Batterie", "12V starter battery"),
    ("Генератор", "Alternator", "Lichtmaschine", "Charging system"),
    ("Стартер", "Starter motor", "Anlasser", "Starting system"),
    ("Запобіжник", "Fuse", "Sicherung", "Electrical protection"),
    ("Електропроводка", "Wiring harness", "Kabelbaum", "Electrical"),
    ("Блок керування двигуном", "Engine control unit", "Motorsteuergerät", "EN abbr. ECU"),
    ("Датчик", "Sensor", "Sensor", "Used across many systems"),
    ("Бортовий комп'ютер", "On-board computer", "Bordcomputer", "Trip data + diagnostics"),
    ("Зарядна станція", "Charging station", "Ladestation", "EV infrastructure"),
    ("Тягова батарея", "Traction battery", "Traktionsbatterie", "High-voltage EV pack"),

    # --- Body & exterior ---
    ("Кузов", "Body", "Karosserie", "Vehicle structure"),
    ("Капот", "Hood", "Motorhaube", "UK 'bonnet'"),
    ("Багажник", "Trunk", "Kofferraum", "UK 'boot'"),
    ("Двері", "Door", "Tür", "Body part"),
    ("Бампер", "Bumper", "Stoßstange", "Exterior trim / absorber"),
    ("Крило", "Fender", "Kotflügel", "UK 'wing'"),
    ("Лобове скло", "Windshield", "Windschutzscheibe", "UK 'windscreen'"),
    ("Фара", "Headlight", "Scheinwerfer", "Front lighting"),
    ("Задні ліхтарі", "Tail lights", "Rücklichter", "Rear lighting"),
    ("Дзеркало заднього виду", "Rear-view mirror", "Rückspiegel", "Driver visibility aid"),

    # --- Interior & comfort ---
    ("Салон", "Cabin", "Innenraum", "Vehicle interior"),
    ("Сидіння", "Seat", "Sitz", "Interior"),
    ("Підголівник", "Headrest", "Kopfstütze", "Safety + comfort"),
    ("Ремінь безпеки", "Seat belt", "Sicherheitsgurt", "Mandatory passive safety"),
    ("Панель приладів", "Dashboard", "Armaturenbrett", "Driver interface"),
    ("Спідометр", "Speedometer", "Tachometer", "Speed instrument"),
    ("Тахометр", "Tachometer", "Drehzahlmesser", "Engine-rpm instrument"),
    ("Кондиціонер", "Air conditioning", "Klimaanlage", "EN abbr. AC; DE 'Klima'"),
    ("Опалювач салону", "Cabin heater", "Heizung", "Comfort system"),
    ("Автомагнітола", "Car stereo", "Autoradio", "Infotainment"),

    # --- Safety & driver assistance ---
    ("Подушка безпеки", "Airbag", "Airbag", "Passive safety"),
    ("Антиблокувальна система", "Anti-lock braking system", "Antiblockiersystem", "Abbr. ABS"),
    ("Система курсової стійкості", "Electronic stability control", "Elektronisches Stabilitätsprogramm", "EN abbr. ESC; DE abbr. ESP"),
    ("Антипробуксовочна система", "Traction control system", "Traktionskontrolle", "EN abbr. TCS"),
    ("Круїз-контроль", "Cruise control", "Tempomat", "Driver assistance"),
    ("Система допомоги при паркуванні", "Parking assist", "Parkassistent", "Driver assistance"),
    ("Камера заднього виду", "Backup camera", "Rückfahrkamera", "UK 'reversing camera'"),
    ("Адаптивний круїз-контроль", "Adaptive cruise control", "Adaptiver Tempomat", "EN abbr. ACC"),
    ("Система утримання в смузі", "Lane keeping assist", "Spurhalteassistent", "EN abbr. LKA"),
    ("Сліпа зона", "Blind spot", "Toter Winkel", "Driver visibility limit"),

    # --- Maintenance & service ---
    ("Технічне обслуговування", "Maintenance", "Wartung", "Scheduled service"),
    ("Заміна оливи", "Oil change", "Ölwechsel", "Routine service"),
    ("Моторна олива", "Engine oil", "Motoröl", "Lubricant"),
    ("Антифриз", "Antifreeze", "Frostschutzmittel", "Cooling-system additive"),
    ("Охолоджувальна рідина", "Coolant", "Kühlflüssigkeit", "Cooling system"),
    ("Гальмівна рідина", "Brake fluid", "Bremsflüssigkeit", "Hydraulic fluid"),
    ("Повітряний фільтр", "Air filter", "Luftfilter", "Wear item"),
    ("Масляний фільтр", "Oil filter", "Ölfilter", "Wear item"),
    ("Паливний фільтр", "Fuel filter", "Kraftstofffilter", "Wear item"),
    ("Ремінь ГРМ", "Timing belt", "Zahnriemen", "Engine wear item"),
    ("Шина", "Tire", "Reifen", "UK 'tyre'"),
    ("Колісний диск", "Wheel rim", "Felge", "Wheel part"),
    ("Тиск у шинах", "Tire pressure", "Reifendruck", "Routine check"),

    # --- Fuel & energy ---
    ("Паливо", "Fuel", "Kraftstoff", "General term"),
    ("Бензин", "Petrol", "Benzin", "US 'gasoline'"),
    ("Дизельне пальне", "Diesel fuel", "Dieselkraftstoff", "Fuel type"),
    ("Стиснений природний газ", "Compressed natural gas", "Erdgas", "EN abbr. CNG"),
    ("Автозаправна станція", "Gas station", "Tankstelle", "UK 'petrol station'"),
    ("Октанове число", "Octane rating", "Oktanzahl", "Petrol quality"),
    ("Витрата палива", "Fuel consumption", "Kraftstoffverbrauch", "Measured L/100 km"),
    ("Викиди CO2", "CO2 emissions", "CO2-Emissionen", "Environmental metric"),

    # --- Manufacturing & production ---
    ("Складальний конвеєр", "Assembly line", "Fließband", "Production"),
    ("Автомобільний завод", "Automotive plant", "Automobilwerk", "Production facility"),
    ("Запасні частини", "Spare parts", "Ersatzteile", "Aftermarket / OEM"),
    ("Серійне виробництво", "Mass production", "Serienproduktion", "Manufacturing"),
    ("Контроль якості", "Quality control", "Qualitätskontrolle", "EN abbr. QC"),
    ("Прототип", "Prototype", "Prototyp", "R&D stage"),

    # --- Industry / market ---
    ("Автомобільний дилер", "Car dealer", "Autohändler", "Sales channel"),
    ("Тест-драйв", "Test drive", "Probefahrt", "Pre-purchase"),
    ("Гарантія", "Warranty", "Garantie", "After-sales"),
    ("Лізинг", "Leasing", "Leasing", "Financing model"),
    ("Автострахування", "Car insurance", "Kfz-Versicherung", "Mandatory in most markets"),
    ("Технічний огляд", "Vehicle inspection", "Hauptuntersuchung", "DE abbr. HU / 'TÜV'"),
    ("Свідоцтво про реєстрацію", "Vehicle registration certificate", "Fahrzeugschein", "Legal document"),
]

assert len(ENTRIES) >= 100, f"Need at least 100 entries, got {len(ENTRIES)}"


def build_records() -> list[dict]:
    return [
        {
            "id": idx,
            "ukrainian": ua,
            "english": en,
            "german": de,
            "notes": note,
        }
        for idx, (ua, en, de, note) in enumerate(ENTRIES, start=1)
    ]


def write_xlsx(records: list[dict], path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Glossary"

    header_font = Font(bold=True, color="FFFFFF", size=12)
    header_fill = PatternFill("solid", fgColor="2E5C8A")
    header_align = Alignment(horizontal="center", vertical="center")

    for col_idx, header in enumerate(HEADERS, start=1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_align

    cell_align = Alignment(vertical="center", wrap_text=True)
    for row_idx, rec in enumerate(records, start=2):
        ws.cell(row=row_idx, column=1, value=rec["id"]).alignment = Alignment(
            horizontal="center", vertical="center"
        )
        ws.cell(row=row_idx, column=2, value=rec["ukrainian"]).alignment = cell_align
        ws.cell(row=row_idx, column=3, value=rec["english"]).alignment = cell_align
        ws.cell(row=row_idx, column=4, value=rec["german"]).alignment = cell_align
        ws.cell(row=row_idx, column=5, value=rec["notes"]).alignment = cell_align

    widths = [6, 36, 36, 40, 50]
    for col_idx, width in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    ws.row_dimensions[1].height = 24
    ws.freeze_panes = "A2"

    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)


def write_json(records: list[dict], path: Path) -> None:
    payload = {
        "meta": {
            "title": f"Trilingual {THEME} Glossary",
            "languages": ["Ukrainian", "English", "German"],
            "theme": THEME,
            "total": len(records),
        },
        "entries": records,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_csv(records: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)
        for rec in records:
            writer.writerow(
                [rec["id"], rec["ukrainian"], rec["english"], rec["german"], rec["notes"]]
            )


def main() -> None:
    records = build_records()
    write_xlsx(records, DATA_DIR / "glossary.xlsx")
    write_json(records, DATA_DIR / "glossary.json")
    write_csv(records, DATA_DIR / "glossary.csv")
    print(f"Wrote {len(records)} entries to {DATA_DIR}/glossary.{{xlsx,json,csv}}")


if __name__ == "__main__":
    main()
