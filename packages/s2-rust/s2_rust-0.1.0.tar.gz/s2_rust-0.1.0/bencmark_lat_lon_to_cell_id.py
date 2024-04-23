import time
import s2cell
import s2_rust

NUM_POINTS = 10**7



lats = [55.96197598047027] * NUM_POINTS
lons = [37.35753533375114] * NUM_POINTS
required_level = 17

start = time.time()
cell_id_using_s2_cell = [s2cell.lat_lon_to_cell_id(lat, lon, required_level) for lat, lon in zip(lats, lons)]
print(f"time execution using s2cell: {time.time() - start}")

start = time.time()
cell_id_using_rust_s2_cell = s2_rust.lat_lon_to_cell_id(lats, lons, required_level)
print(f"time execution using s2_rust: {time.time() - start}")

assert cell_id_using_s2_cell == cell_id_using_s2_cell