import random
import csv

OUTPUT_FILE = "skin_data.csv"
NUMBER_OF_ROWS = 15000

SKIN_CONDITIONS = ["acne", "eczema", "psoriasis", "rosacea"]

def generate_random_log():
    skin_condition = random.choice(SKIN_CONDITIONS)

    sleep_hours = round(random.uniform(3, 10), 1)
    stress_level = random.randint(1, 5)
    water_intake_litres = round(random.uniform(0.5, 4.0), 1)
    diet_quality = random.randint(1, 5)
    symptom_severity = random.randint(1, 5)
    temperature = round(random.uniform(-2, 35), 1)
    humidity = round(random.uniform(20, 95), 1)

    return {
        "skinConditionType": skin_condition,
        "sleepHours": sleep_hours,
        "stressLevel": stress_level,
        "waterIntakeLitres": water_intake_litres,
        "dietQuality": diet_quality,
        "symptomSeverity": symptom_severity,
        "temperature": temperature,
        "humidity": humidity,
    }

def calculate_risk_level(log):
    condition = log["skinConditionType"]

    sleep = log["sleepHours"]
    stress = log["stressLevel"]
    water = log["waterIntakeLitres"]
    diet = log["dietQuality"]
    symptoms = log["symptomSeverity"]
    temperature = log["temperature"]
    humidity = log["humidity"]

    score = 0

    if symptoms >= 4:
        score += 3
    elif symptoms == 3:
        score += 2

    if stress >= 4:
        score += 2
    elif stress == 3:
        score += 1

    if condition == "acne":
        if diet <= 2:
            score += 2
        if sleep < 6:
            score += 2

    elif condition == "eczema":
        if water < 2:
            score += 2
        if humidity > 75:
            score += 2

    elif condition == "psoriasis":
        if sleep < 6:
            score += 2
        if temperature < 8 or humidity < 35:
            score += 2

    elif condition == "rosacea":
        if temperature > 25:
            score += 2
        if water < 2:
            score += 1

    if score >= 7:
        return "High"
    elif score >= 4:
        return "Medium"
    else:
        return "Low"
    
def generate_dataset():
    columns = [
        "skinConditionType",
        "sleepHours",
        "stressLevel",
        "waterIntakeLitres",
        "dietQuality",
        "symptomSeverity",
        "temperature",
        "humidity",
        "riskLevel",
    ]

    with open(OUTPUT_FILE, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

        for _ in range(NUMBER_OF_ROWS):
            log = generate_random_log()
            log["riskLevel"] = calculate_risk_level(log)
            writer.writerow(log)

    print(f"Dataset created successfully: {OUTPUT_FILE}")
    print(f"Total rows created: {NUMBER_OF_ROWS}")

if __name__ == "__main__":
    generate_dataset()

