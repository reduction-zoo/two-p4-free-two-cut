import Challenge
open TwoP4FreeTwoCut
example : legalTarget ⟨8, [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7)]⟩ = true := by native_decide
example : avoids (pathUnion 2 4) (pathUnion 2 4) = false := by native_decide
