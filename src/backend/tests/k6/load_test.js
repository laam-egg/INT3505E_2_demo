import http from 'k6/http';
import { check, sleep } from 'k6';

// --- Test configuration ---
export const options = {
  vus: 10,               // number of virtual users
  duration: '30s',       // test duration
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests should respond <500ms
    http_req_failed: ['rate<0.01'],   // <1% of requests should fail
  },
};

// --- Test logic ---
export default function () {
  const res = http.get('http://localhost:5000/');

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response is not empty': (r) => r.body && r.body.length > 0,
  });

  sleep(1); // simulate user think time
}
