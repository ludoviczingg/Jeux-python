import pandas as pd
from bird import Bird  # Assure-toi que la classe Bird est bien définie dans game_classes.py

def load_birds_from_excel(filepath):
    try:
        df = pd.read_excel(filepath)
    except Exception as e:
        print(f"Erreur lors du chargement du fichier : {e}")
        return []

    bird_list = []

    for _, row in df.iterrows():
        try:
            bird = Bird(
                common_name=row["Common name"],
                color=row["Color"],
                power_text=row["Power text"],
                flavor_text=row["Flavor text"],
                predator=row["Predator"],
                flocking=row["Flocking"],
                bonus_card=row["Bonus card"],
                victory_point=row["Victory points"],
                nest_type=row["Nest type"],
                egg_limit=row["Egg limit"],
                wingspan=row["Wingspan"],
                forest=row["Forest"],
                grassland=row["Grassland"],
                wetland=row["Wetland"],
                invertebrate=row["Invertebrate"],
                seed=row["Seed"],
                fish=row["Fish"],
                fruit=row["Fruit"],
                rodent=row["Rodent"],
                wild_food=row["Wild (food)"],
                food_cost=row["/ (food cost)"],
                total_food=row["Total food cost"],
                swift_start=row["Swift Start"]                
            )
            bird_list.append(bird)
        except Exception as e:
            print(f"Erreur lors du traitement d’un oiseau : {e}")
            continue
     

    return bird_list

