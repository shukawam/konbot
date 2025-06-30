import { sleep } from 'k6';
import http from 'k6/http';

const baseUrl = 'http://gateway:8000/v1';

export const options = {
    vus: 1,
    duration: '10m',
}

export default function () {
    getPing();
    sleep(1);
}

const getPing = () => http.get(`${baseUrl}/ping`);
