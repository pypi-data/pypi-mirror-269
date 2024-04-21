from fastapi import FastAPI

import mychef.access.api
import mychef.recipes.api
from mychef.__about__ import __version__


def get_app() -> FastAPI:
    """Build and configure application server."""
    app = FastAPI(
        docs_url="/api/docs",
        title="MyChef",
        version=__version__,
        summary="Recipe recommendation application.",
        license_info={
            "name": "GNU Affero General Public License (AGPL)",
            "url": "https://www.gnu.org/licenses/agpl-3.0.html",
        },
    )

    app.include_router(mychef.access.api.router, prefix="/api")
    app.include_router(mychef.recipes.api.router, prefix="/api")

    return app


app = get_app()
