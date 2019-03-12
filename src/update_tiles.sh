#!bin/bash

export env $(cat ./src/.env | xargs) rails

mapbox datasets create-tileset 'cjspu92j73bax33t6xi5pdeao' pvgelder.cjspu92j73bax33t6xi5pdeao-3008v

mapbox datasets create-tileset 'cjspueidg064y33nzn5m6ii24' pvgelder.cjspueidg064y33nzn5m6ii24-0rvbk

mapbox datasets create-tileset 'cjspwm4jw06nz2rnyxnpnt31g' pvgelder.cjspwm4jw06nz2rnyxnpnt31g-153u6

mapbox datasets create-tileset 'cjspu9epe38b02wqf7fcfi05q' pvgelder.cjspu9epe38b02wqf7fcfi05q-2eoh8
