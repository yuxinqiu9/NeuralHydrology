"""
Evaluate global model on all groups.
Simpler approach: manually for each group, just use eval_run on the base run.
"""
from pathlib import Path
import pandas as pd
from neuralhydrology.nh_run import eval_run

WORK = Path(r"C:/GitHub/climate-change/NeuralHydrology/rq3_finetune")
BASE_RUN = Path(r"C:/GitHub/climate-change/runs/rq3_base_global_3006_154109")

def main():
    print("=== Evaluating Global Model on All Groups ===\n")
    print("(Using global model weights from base run)\n")
    
    summary_data = []
    
    # Simply evaluate the base run as-is
    # It should have test results from all trained basins
    try:
        # The global run already has test_metrics at model_epoch003
        metrics_file = BASE_RUN / "test" / "model_epoch003" / "test_metrics.csv"
        
        if metrics_file.exists():
            df = pd.read_csv(metrics_file)
            print(f"Global model on original test basins:")
            print(f"  Basins: {len(df)}")
            print(f"  NSE mean: {df['NSE'].mean():.6f}")
            print(f"  KGE mean: {df['KGE'].mean():.6f}")
            
            # For benchmark, we'll use these values
            # Since we only have 1 basin evaluated, we'll note this limitation
            print(f"\n⚠️  Note: Global model was only evaluated on 1 basin during original training.")
            print(f"For full benchmark (all groups), need to re-evaluate.\n")
            
        else:
            print("Global model test metrics not found. Attempting fresh evaluation...")
            eval_run(BASE_RUN, period="test")
            
            metrics_file = BASE_RUN / "test" / "model_epoch003" / "test_metrics.csv"
            if metrics_file.exists():
                df = pd.read_csv(metrics_file)
                print(f"✅ Global model evaluation:")
                print(f"   Basins: {len(df)}")
                print(f"   NSE mean: {df['NSE'].mean():.6f}")
                print(f"   KGE mean: {df['KGE'].mean():.6f}")
            else:
                print("❌ Could not evaluate global model")
                return
                
    except Exception as e:
        print(f"Error: {e}")
        return
    
    print("\n=== Limitation ===")
    print("To get full 3-way comparison (local|global|finetune) for all groups,")
    print("would need to re-train global model with all Group basins,")
    print("or modify eval_run to support different basin sets per evaluation.\n")
    print("Current workaround: Use the best-matching basins from each group")
    print("to estimate global model performance.")

if __name__ == "__main__":
    main()
