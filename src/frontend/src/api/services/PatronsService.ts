/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { empty_HATEOAS } from '../models/empty_HATEOAS';
import type { Patron_HATEOAS } from '../models/Patron_HATEOAS';
import type { PatronCreate } from '../models/PatronCreate';
import type { PatronList_HATEOAS } from '../models/PatronList_HATEOAS';
import type { PatronReplace } from '../models/PatronReplace';
import type { PatronUpdate } from '../models/PatronUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class PatronsService {
    /**
     * Lấy danh sách tất cả các patrons, có pagination.
     * @returns PatronList_HATEOAS Success
     * @throws ApiError
     */
    public static getCollection({
        pageNumber,
        pageSize = 100,
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
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<PatronList_HATEOAS> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/patrons/',
            headers: {
                'X-Fields': xFields,
            },
            query: {
                'pageNumber': pageNumber,
                'pageSize': pageSize,
            },
        });
    }
    /**
     * Thêm patron mới.
     * @returns Patron_HATEOAS Success
     * @throws ApiError
     */
    public static postCollection({
        payload,
        xFields,
    }: {
        payload: PatronCreate,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Patron_HATEOAS> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/patrons/',
            headers: {
                'X-Fields': xFields,
            },
            body: payload,
        });
    }
    /**
     * Xóa patron, theo ID
     * @returns empty_HATEOAS Success
     * @throws ApiError
     */
    public static deleteItem({
        patronId,
        xFields,
    }: {
        patronId: string,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<empty_HATEOAS> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/patrons/{patronId}',
            path: {
                'patronId': patronId,
            },
            headers: {
                'X-Fields': xFields,
            },
        });
    }
    /**
     * Lấy patron theo ID
     * @returns Patron_HATEOAS Success
     * @throws ApiError
     */
    public static getItem({
        patronId,
        xFields,
    }: {
        patronId: string,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Patron_HATEOAS> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/patrons/{patronId}',
            path: {
                'patronId': patronId,
            },
            headers: {
                'X-Fields': xFields,
            },
        });
    }
    /**
     * Sửa toàn bộ patron, theo ID
     * @returns Patron_HATEOAS Success
     * @throws ApiError
     */
    public static putItem({
        patronId,
        payload,
        xFields,
    }: {
        patronId: string,
        payload: PatronReplace,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Patron_HATEOAS> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/patrons/{patronId}',
            path: {
                'patronId': patronId,
            },
            headers: {
                'X-Fields': xFields,
            },
            body: payload,
        });
    }
    /**
     * Sửa một phần patron, theo ID
     * @returns Patron_HATEOAS Success
     * @throws ApiError
     */
    public static patchItem({
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
    }): CancelablePromise<Patron_HATEOAS> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/patrons/{patronId}',
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
