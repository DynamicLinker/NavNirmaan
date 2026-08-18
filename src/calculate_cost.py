import pickle
import pandas as pd
import os

def calculate_cost(bathrooms: int, bedrooms: int, rooms: int, area: float) -> float:
    """
    Load the house_construction_model.pkl and predict the cost based on the structured data.
    """
    model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'house_construction_model.pkl')
    
    if not os.path.exists(model_path):
        print(f"Warning: Model file not found at {model_path}")
        return 0.0

    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
            
        # Create a DataFrame with the exact feature names the user provided.
        # This helps in case the model was trained with pandas and expects specific column names.
        input_df = pd.DataFrame([{
            'bathrooms': bathrooms,
            'bedrooms': bedrooms,
            'rooms': rooms,
            'area': area
        }])
        
        # In case the model expects a numpy array, we also provide a fallback.
        try:
            prediction = model.predict(input_df)
        except Exception as e:
            # Fallback to numpy array if DataFrame fails (e.g., mismatch in column names or model type)
            prediction = model.predict(input_df.values)
            
        return float(prediction[0])
    except Exception as e:
        print(f"Error calculating cost: {e}")
        return 0.0
