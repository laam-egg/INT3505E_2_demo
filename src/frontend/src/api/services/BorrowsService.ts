/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Borrow_HATEOAS } from '../models/Borrow_HATEOAS';
import type { BorrowCreate } from '../models/BorrowCreate';
import type { BorrowList_HATEOAS } from '../models/BorrowList_HATEOAS';
import type { BorrowUpdate } from '../models/BorrowUpdate';
import type { empty_HATEOAS } from '../models/empty_HATEOAS';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class BorrowsService {
    /**
     * Lấy danh sách tất cả các borrows, có pagination. Có thể lọc theo patronId.
     * @returns BorrowList_HATEOAS Success
     * @throws ApiError
     */
    public static getCollection({
        pageNumber,
        pageSize = 100,
        patronId,
        copyId,
        xFields,
    }: {
        /**
         * Page number
         */
        pageNumber?: number,
        /**
         * Page size
         */
        pageSize?: number,
        /**
         * Patron ID (optional)
         */
        patronId?: string,
        /**
         * Copy ID (optional)
         */
        copyId?: string,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<BorrowList_HATEOAS> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/borrows/',
            headers: {
                'X-Fields': xFields,
            },
            query: {
                'pageNumber': pageNumber,
                'pageSize': pageSize,
                'patronId': patronId,
                'copyId': copyId,
            },
        });
    }
    /**
     * Thêm borrow mới.
     * @returns Borrow_HATEOAS Success
     * @throws ApiError
     */
    public static postCollection({
        payload,
        xFields,
    }: {
        payload: BorrowCreate,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Borrow_HATEOAS> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/borrows/',
            headers: {
                'X-Fields': xFields,
            },
            body: payload,
        });
    }
    /**
     * Xóa borrow, theo ID
     * @returns empty_HATEOAS Success
     * @throws ApiError
     */
    public static deleteItem({
        borrowId,
        xFields,
    }: {
        borrowId: string,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<empty_HATEOAS> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/borrows/{borrowId}',
            path: {
                'borrowId': borrowId,
            },
            headers: {
                'X-Fields': xFields,
            },
        });
    }
    /**
     * Lấy borrow theo ID
     * @returns Borrow_HATEOAS Success
     * @throws ApiError
     */
    public static getItem({
        borrowId,
        xFields,
    }: {
        borrowId: string,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Borrow_HATEOAS> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/borrows/{borrowId}',
            path: {
                'borrowId': borrowId,
            },
            headers: {
                'X-Fields': xFields,
            },
        });
    }
    /**
     * Sửa một phần borrow, theo ID
     * @returns Borrow_HATEOAS Success
     * @throws ApiError
     */
    public static patchItem({
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
    }): CancelablePromise<Borrow_HATEOAS> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/borrows/{borrowId}',
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
