#!/usr/bin/env python3
"""Quick test script to verify the game runs"""

from src.wizards_workshop import main

if __name__ == "__main__":
    print("Starting Wizard's Workshop...")
    print("\nControls:")
    print("- Click cards to pick them up")
    print("- Click again to drop them")  
    print("- Drop cards on the glowing stations to combine them")
    print("\nStarting Recipes:")
    print("- Forge: Iron Ore + Coal = Iron Ingot")
    print("- Study: Mysterious Tome = Basic Forging Knowledge")
    print("\nResources spawn automatically from generators!")
    
    main()