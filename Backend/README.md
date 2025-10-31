#Backend part of Steam Wishlist

In the project directory, you can run: 
### `uvicorn main:app`
It runs the backend app.

Backend app saves gathered wishlists at `Wishlist/` directory,
and game info at `Gamelists/` directory in JSON format. Gathered lists are used
by app only during the day the info was gathered into them.

