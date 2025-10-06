/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Borrow } from '../models/Borrow';
import type { BorrowCreate } from '../models/BorrowCreate';
import type { BorrowUpdate } from '../models/BorrowUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class BorrowsService {
    /**
     * Get all borrows with optional patron filtering
     * @returns Borrow Success
     * @throws ApiError
     */
    public static getAllBorrows({
        patronId,
        xFields,
    }: {
        /**
         * Filter by patron ID
         */
        patronId?: string,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Array<Borrow>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/borrows/',
            headers: {
                'X-Fields': xFields,
            },
            query: {
                'patronId': patronId,
            },
        });
    }
    /**
     * Create a new borrow
     * @returns Borrow Success
     * @throws ApiError
     */
    public static createANewBorrow({
        payload,
        xFields,
    }: {
        payload: BorrowCreate,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Borrow> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/borrows/',
            headers: {
                'X-Fields': xFields,
            },
            body: payload,
        });
    }
    /**
     * Delete a borrow
     * @returns any Success
     * @throws ApiError
     */
    public static deleteBorrowById({
        borrowId,
    }: {
        borrowId: string,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/borrows/{borrowId}',
            path: {
                'borrowId': borrowId,
            },
        });
    }
    /**
     * Get a specific borrow by ID
     * @returns Borrow Success
     * @throws ApiError
     */
    public static getBorrowById({
        borrowId,
        xFields,
    }: {
        borrowId: string,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Borrow> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/borrows/{borrowId}',
            path: {
                'borrowId': borrowId,
            },
            headers: {
                'X-Fields': xFields,
            },
        });
    }
    /**
     * Update borrow status
     * @returns Borrow Success
     * @throws ApiError
     */
    public static updateBorrowStatusById({
        borrowId,
        payload,
        xFields,
    }: {
        borrowId: string,
        payload: BorrowUpdate,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Borrow> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/borrows/{borrowId}',
            path: {
                'borrowId': borrowId,
            },
            headers: {
                'X-Fields': xFields,
            },
            body: payload,
        });
    }
}
