import express, { Express, Request, Response } from 'express';
import dotenv from 'dotenv';
import { JWT } from './jwt';
dotenv.config();

const JWT_SECRET_KEY = process.env.JWT_SECRET_KEY || "";
if (!JWT_SECRET_KEY) {
    throw new Error("Environment variable JWT_SECRET_KEY is invalid or missing.");
}

let jwt = new JWT(JWT_SECRET_KEY);

const app: Express = express();
const port = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req: Request, res: Response) => {
    res.send('Welcome');
});

app.post('/sign', (req: Request, res: Response) => {
    res.send(
        jwt.sign(req.body)
    );
});

app.post('/verify', (req: Request, res: Response) => {
    res.send(jwt.verify(req.body.token));
});

app.post('/change-key', (req: Request, res: Response) => {
    jwt = new JWT(JWT_SECRET_KEY + `${new Date()}`);
    res.send("{}");
});

app.listen(port, () => {
    console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
});
