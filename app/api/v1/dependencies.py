from fastapi import Depends

from app.db.session import get_db
from app.core.auth import get_current_user


DBSession = Depends(get_db)
CurrentUser = Depends(get_current_user)
