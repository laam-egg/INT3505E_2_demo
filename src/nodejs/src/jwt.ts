import jwt from 'jsonwebtoken';

export class JWT {
    public constructor(private secretKey: string) {}

    public sign(payload: string | object) {
        return jwt.sign(payload, this.secretKey, {
            algorithm: 'HS256',
        });
    }

    public verify(token: string) {
        try {
            const verified = jwt.verify(token, this.secretKey, {
                algorithms: ['HS256'],
            });
            
            return {
                status: "verified",
                payload: verified,
            };
        } catch (e) {
            const decoded = jwt.decode(token);

            return {
                status: "invalid",
                details: "" + e,
                payload: decoded,
            };
        }
    }
}
