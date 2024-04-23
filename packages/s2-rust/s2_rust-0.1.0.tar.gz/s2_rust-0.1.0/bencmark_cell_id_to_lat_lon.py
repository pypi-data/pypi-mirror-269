import time
import s2cell
import s2_rust

NUM_POINTS = 10**6



s2_cell_id_arr = [5095047777373650944] * NUM_POINTS
required_level = 17

start = time.time()
lat_lon_using_s2_cell = [s2cell.cell_id_to_lat_lon(cell_id) for cell_id in s2_cell_id_arr]
print(f"time execution using s2cell: {time.time() - start}")

start = time.time()
lat_lon_using_s2_rust = s2_rust.cell_id_to_lat_lon(s2_cell_id_arr)
print(f"time execution using s2_rust: {time.time() - start}")

assert lat_lon_using_s2_cell == lat_lon_using_s2_rust