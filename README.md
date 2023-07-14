# post_man
Post man is a multi-threaded, multi-sensor querier. It makes use of a Leader per
type of sensor, with as many workers as sensors. It queries them periodically
injecting the results of the queries into a PostGreSQL DB with a specified format.

# Known bugs
- iot sensors failing and not knowing which one it is.