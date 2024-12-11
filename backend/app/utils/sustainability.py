class SustainabilityUtils:
    @staticmethod
    def calculate_carbon_footprint(transportation_miles, energy_consumption_kwh, waste_generated_kg):
        """
        Calculate the carbon footprint based on transportation, energy consumption, and waste generation.
        
        Parameters:
        - transportation_miles (float): The number of miles traveled by car.
        - energy_consumption_kwh (float): The amount of energy consumed in kilowatt-hours.
        - waste_generated_kg (float): The amount of waste generated in kilograms.

        Returns:
        - float: The estimated carbon footprint in kilograms of CO2 equivalent.
        """
        # Constants for carbon footprint calculations
        CO2_PER_MILE = 0.404  # kg CO2 per mile for an average car
        CO2_PER_KWH = 0.92    # kg CO2 per kWh for average electricity generation
        CO2_PER_KG_WASTE = 0.5 # kg CO2 per kg of waste

        transportation_footprint = transportation_miles * CO2_PER_MILE
        energy_footprint = energy_consumption_kwh * CO2_PER_KWH
        waste_footprint = waste_generated_kg * CO2_PER_KG_WASTE

        total_footprint = transportation_footprint + energy_footprint + waste_footprint
        return total_footprint

    @staticmethod
    def assess_sustainability_practices(practices):
        """
        Assess sustainability practices based on a list of practices.
        
        Parameters:
        - practices (list): A list of sustainability practices (e.g., recycling, using public transport).

        Returns:
        - dict: A summary of the sustainability assessment.
        """
        assessment = {
            "recycling": "Not Implemented",
            "public_transport": "Not Implemented",
            "energy_efficiency": "Not Implemented",
            "sustainable_food": "Not Implemented",
        }

        if "recycling" in practices:
            assessment["recycling"] = "Implemented"
        if "public_transport" in practices:
            assessment["public_transport"] = "Implemented"
        if "energy_efficiency" in practices:
            assessment["energy_efficiency"] = "Implemented"
        if "sustainable_food" in practices:
            assessment["sustainable_food"] = "Implemented"

        return assessment

# Example usage
if __name__ == "__main__":
    # Calculate carbon footprint
    footprint = SustainabilityUtils.calculate_carbon_footprint(
        transportation_miles=100,
        energy_consumption_kwh=300,
        waste_generated_kg=50
    )
    print(f"Estimated Carbon Footprint: {footprint:.2f} kg CO2e")

    # Assess sustainability practices
    practices = ["recycling", "public_transport"]
    assessment = SustainabilityUtils.assess_sustainability_practices(practices)
    print("Sustainability Assessment:", assessment)
