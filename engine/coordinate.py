class SearchArea:
    def __init__(self, x, y, radius=1000):
        # Used this for reference (NOAA endorsed): http://edwilliams.org/gccalc.htm

        # Define the given coordinates and radius
        self.x = int(x)
        self.y = int(y)
        # In feet. With conversion, 1000 ft here = 1000.0022039091077 ft. 0.0002% error for Toledo. 0.03% error for Dayton.
        # The error is not really a big deal, it's just to ~roughly~ convert a tangible number of feet to an area we can search.
        # 1000ft radius is a big enough area for an "approximate location", I think. Depends on how many SSIDs we find in that area.
        self.radius = int(radius)
        feet_per_second = 364391   # conversion factor

        # Calculate the delta of the coordinates
        delta = self.radius / feet_per_second      # in seconds

        # Generate the new coordinate pairs
        self.lat1 = x - delta
        self.long1 = y - delta
        self.lat2 = x + delta
        self.long2 = y + delta
