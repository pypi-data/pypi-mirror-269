use routrs::maritime;
use routrs::prelude::*;

pub fn distance(origin: &Geoloc, destination: &Geoloc) -> DistanceResult {
    maritime::distance(origin, destination)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_calculates_maritime_distance() {
        let from: Geoloc = (40.6759, -74.0504); // USNYC
        let to: Geoloc = (41.0067858, 28.9732219); // TRIST
        let (distance, path, path_type) = distance(&from, &to).unwrap();

        assert_eq!(distance, 9224.95741604269);
        assert_eq!(path.len(), 118);
        assert_eq!(path_type, PathType::ViaWaypoints);
    }
}
