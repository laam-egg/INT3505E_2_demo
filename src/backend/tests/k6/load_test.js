/**
 * Each iteration creates 1 request and wait 1 second.
 * In the test duration of 30s, each VU runs about 30 requests.
 * That does not cross the rate limit (50 reqs/min)
 * so this test should success, provided that the
 * environment variable RATE_LIMIT_BY_X_FORWARDED_FOR
 * is set to True.
 */

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
  // Generate a fake but unique IPv4 per VU
  /**
   * Gemini:
   * 
   * In k6, __VU is an execution context variable that provides
   * information about the current Virtual User (VU).
   * 
   * Specifically, __VU represents the ID of the current Virtual User.
   * 
   * Each VU in a k6 test script runs independently, simulating
   * a separate user interacting with your system. The __VU variable
   * allows you to differentiate between these individual VUs during
   * test execution.
   */
  const ip = `10.0.${Math.floor(__VU / 256)}.${__VU % 256}`;

  const headers = {
    'X-Forwarded-For': ip,
  };

  const res = http.get('http://localhost:5000/', { headers });

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response is not empty': (r) => r.body && r.body.length > 0,
  });

  sleep(1); // simulate user think time
}
