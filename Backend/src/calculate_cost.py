import joblib
import pandas as pd
import os
import math

def calculate_cost(bathrooms: int, bedrooms: int, rooms: int, area: float, city: str) -> float:
    """
    Load the house_construction_model.pkl and predict the cost based on the structured data.
    """
    model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'house_construction_model.pkl')
    
    if not os.path.exists(model_path):
        print(f"Warning: Model file not found at {model_path}")
        return 0.0

    try:
        model = joblib.load(model_path)
            
        # Geometric calculation for vertical walls (from OpenSCAD model constraints)
        outer_perimeter = 4 * math.sqrt(area)
        internal_walls = (rooms - 1) * math.sqrt(area / rooms) if rooms > 0 else 0
        total_wall_length = outer_perimeter + internal_walls
        
        wall_h = 9.0
        wall_t = 0.5
        wall_volume_cft = total_wall_length * wall_h * wall_t
        
        # ~10 bricks per cubic foot of brickwork, ~0.05 bags cement per brick
        bricks_quantity = int(wall_volume_cft * 10)
        cement_bags = bricks_quantity * 0.05
            
        # Core features calculated from user input and geometry
        core_features = {
            'built_up_area_sqft': area,
            'floors': 1,
            'rooms': rooms,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'cement_bags': cement_bags,
            'bricks_quantity': bricks_quantity,
            'city': city
        }
        
        dataset_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'indian_house_construction_dataset_1000.csv')
        if os.path.exists(dataset_path):
            try:
                df_hist = pd.read_csv(dataset_path)
                # Select only numeric columns and calculate their mean
                numeric_cols = df_hist.select_dtypes(include=['number']).mean().to_dict()
                
                # The model might also expect categorical columns like city/state. We pick the mode (most common).
                mode_cols = df_hist.select_dtypes(exclude=['number']).mode().iloc[0].to_dict()
                if 'house_id' in mode_cols:
                    del mode_cols['house_id'] # ID is irrelevant
                    
                # Merge all defaults, then overwrite with our core features (including city)
                final_features = {**numeric_cols, **mode_cols}
                for k, v in core_features.items():
                    final_features[k] = v
                    
                input_df = pd.DataFrame([final_features])
            except Exception as e:
                print(f"Warning: Could not parse dataset for padding: {e}")
                input_df = pd.DataFrame([core_features])
        else:
            input_df = pd.DataFrame([core_features])
        
        # We will attempt prediction.
        try:
            prediction = model.predict(input_df)
        except Exception as e:
            # Fallback to values array if column names don't match or Pipeline fails
            prediction = model.predict(input_df.values)
            
        import numpy as np
        # The model might predict multiple targets (e.g., [cost_per_sqft, material_cost, total_cost]).
        # The total cost is mathematically the largest value.
        pred_array = np.array(prediction)
        return float(np.max(pred_array))
    except Exception as e:
        print(f"Error calculating cost: {e}")
        return 0.0
