## MMDA Traffic API

An API wrapper for TV5-MMDA's Traffic Monitoring API.  
Built to add more useful endpoints.

## Usage

### Highways

```GET /v1/highways```  
Get list of monitored highways.

### Segments

```GET /v1/segments```  
Get list of segments.

```GET /v1/highways/<highway_id>/segments```  
Get list of segments in a highway.

### Traffic

```GET /v1/traffic```  
Get all traffic details.

```GET /v1/highways/<highway_id>/traffic```  
GET traffic details of a highway.

```GET /v1/segments/<segment_id>/traffic```  
GET traffic details of a highway segment.

### Traffic Filtering

Filter traffic result by direction or by traffic status.
Append a query string to any traffic endpoint.

```
?direction=<direction>
?status=<status>
?direction=<direction>&status=<status>
```

#### Direction codes

NB: Northbound  
SB: Southbound

#### Status codes

L: Light  
ML: Light to Moderate  
M: Moderate  
MH: Moderate to Heavy  
H: Heavy

## Development Setup

Make a copy of `example.env` named `.env`. Updated `.env` file if needed.

## Acknowledgement

Inspired by [Ridvan Baluyos](https://github.com/ridvanbaluyos/)' [traffic-api](https://github.com/ridvanbaluyos/traffic-api/) written in PHP.

## Licence

Open-sourced software licensed under the [MIT license](https://choosealicense.com/licenses/mit/).

Copyright (c) 2017 Dhan-Rheb Belza
