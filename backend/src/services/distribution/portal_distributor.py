from uuid import UUID
from datetime import datetime
from backend.src.models.entities import ReportStatus, Report
from backend.src.core.database import SessionLocal
from sqlalchemy.future import select
from sqlalchemy import update

class PortalDistributor:
    async def distribute(self, report_id: UUID, distributor_id: UUID) -> bool:
        async with SessionLocal() as session:
            result = await session.execute(select(Report).filter(Report.id == report_id))
            report = result.scalar_one_or_none()
            if not report:
                return False
            # Mark the report as distributed in the portal
            await session.execute(
                update(Report)
                .where(Report.id == report_id)
                .values(status=ReportStatus.DISTRIBUTED, distributed_at=datetime.utcnow())
            )
            await session.commit()
            return True
