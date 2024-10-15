from src.model.database import db
from src.model.riders.tables.rider_guardian import RiderGuardian

def assign_guardian_to_rider(rider_id: int, guardian_id: int, relationship: str) -> RiderGuardian:
    rider_guardian = RiderGuardian(
        rider_id=rider_id,
        guardian_id=guardian_id,
        relationship=relationship  # Assign the relationship value here
    )
    db.session.add(rider_guardian)
    db.session.commit()
    db.session.expunge(rider_guardian)
    return rider_guardian
