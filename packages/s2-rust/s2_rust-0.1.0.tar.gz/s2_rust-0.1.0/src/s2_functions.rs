use s2::{cellid::CellID, latlng::LatLng};

pub fn lat_lon_to_cell_id_one_point(lat: f64, lon: f64, level: u64) -> u64 {
    let lat_lng = LatLng::from_degrees(lat, lon);
    let cell_id = CellID::from(lat_lng);
    cell_id.parent(level).0
}

pub fn cell_id_to_lat_lon_one_point(cell_id: u64) -> (f64, f64) {
    let lat_lng = LatLng::from(CellID(cell_id));
    (lat_lng.lat.deg(), lat_lng.lng.deg())
}

#[cfg(test)]
mod tests {
    use crate::s2_functions::lat_lon_to_cell_id_one_point;

    #[test]
    fn test_lat_lon_to_cell_id_works() {
        assert_eq!(lat_lon_to_cell_id_one_point(55.96197598047027, 37.35753533375114, 17), 5095047777373650944);
    }

    #[test]
    fn test_cell_id_to_lat_lon_works() {
        assert_eq!(cell_id_to_lat_lon_one_point(5095047777373650944), (55.96197598047027, 37.35753533375114));
    }
    
}