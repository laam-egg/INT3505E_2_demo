/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Patron } from '../models/Patron';
import type { PatronCreate } from '../models/PatronCreate';
import type { PatronUpdate } from '../models/PatronUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class PatronsService {
    /**
     * Get all patrons with pagination
     * @returns Patron Success
     * @throws ApiError
     */
    public static getAllPatrons({
        xFields,
    }: {
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Array<Patron>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/patrons/',
            headers: {
                'X-Fields': xFields,
            },
        });
    }
    /**
     * Create a new patron
     * @returns Patron Success
     * @throws ApiError
     */
    public static createANewPatron({
        payload,
        xFields,
    }: {
        payload: PatronCreate,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Patron> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/patrons/',
            headers: {
                'X-Fields': xFields,
            },
            body: payload,
        });
    }
    /**
     * Delete a patron
     * @returns any Success
     * @throws ApiError
     */
    public static deletePatronById({
        patronId,
    }: {
        patronId: string,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/patrons/{patronId}',
            path: {
                'patronId': patronId,
            },
        });
    }
    /**
     * Get a specific patron by ID
     * @returns Patron Success
     * @throws ApiError
     */
    public static getPatronById({
        patronId,
        xFields,
    }: {
        patronId: string,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Patron> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/patrons/{patronId}',
            path: {
                'patronId': patronId,
            },
            headers: {
                'X-Fields': xFields,
            },
        });
    }
    /**
     * Update a patron
     * @returns Patron Success
     * @throws ApiError
     */
    public static updatePatronById({
        patronId,
        payload,
        xFields,
    }: {
        patronId: string,
        payload: PatronUpdate,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Patron> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/patrons/{patronId}',
            path: {
                'patronId': patronId,
            },
            headers: {
                'X-Fields': xFields,
            },
            body: payload,
        });
    }
}
