import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    vus: 10,  // Number of virtual users
    duration: '30s',  // Test duration
};

export default function () {
    let res = http.get('http://localhost:8000/list_sut');

    // Check if the response status is 200
    check(res, {
        'is status 200': (r) => r.status === 200,
        'response time < 500ms': (r) => r.timings.duration < 500,
    });

    sleep(1);  // Simulate user wait time before the next request
}
