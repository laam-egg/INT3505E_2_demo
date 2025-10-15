/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Copy_HATEOAS } from '../models/Copy_HATEOAS';
import type { CopyCreate } from '../models/CopyCreate';
import type { CopyList_HATEOAS } from '../models/CopyList_HATEOAS';
import type { CopyReplace } from '../models/CopyReplace';
import type { CopyUpdate } from '../models/CopyUpdate';
import type { empty_HATEOAS } from '../models/empty_HATEOAS';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class CopiesService {
    /**
     * Lấy danh sách tất cả các copies của một title, có pagination.
     * @returns CopyList_HATEOAS Success
     * @throws ApiError
     */
    public static getCollection({
        titleId,
        pageNumber,
        pageSize = 100,
        xFields,
    }: {
        titleId: string,
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
    }): CancelablePromise<CopyList_HATEOAS> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/titles/{titleId}/copies/',
            path: {
                'titleId': titleId,
            },
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
     * Thêm bản sao mới cho một đầu sách.
     * @returns Copy_HATEOAS Success
     * @throws ApiError
     */
    public static postCollection({
        titleId,
        payload,
        xFields,
    }: {
        titleId: string,
        payload: CopyCreate,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Copy_HATEOAS> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/titles/{titleId}/copies/',
            path: {
                'titleId': titleId,
            },
            headers: {
                'X-Fields': xFields,
            },
            body: payload,
        });
    }
    /**
     * Xóa copy, theo ID
     * @returns empty_HATEOAS Success
     * @throws ApiError
     */
    public static deleteItem({
        titleId,
        copyId,
        xFields,
    }: {
        titleId: string,
        copyId: string,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<empty_HATEOAS> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/titles/{titleId}/copies/{copyId}',
            path: {
                'titleId': titleId,
                'copyId': copyId,
            },
            headers: {
                'X-Fields': xFields,
            },
        });
    }
    /**
     * Lấy copy theo ID
     * @returns Copy_HATEOAS Success
     * @throws ApiError
     */
    public static getItem({
        titleId,
        copyId,
        xFields,
    }: {
        titleId: string,
        copyId: string,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Copy_HATEOAS> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/titles/{titleId}/copies/{copyId}',
            path: {
                'titleId': titleId,
                'copyId': copyId,
            },
            headers: {
                'X-Fields': xFields,
            },
        });
    }
    /**
     * Sửa toàn bộ copy, theo ID
     * @returns Copy_HATEOAS Success
     * @throws ApiError
     */
    public static putItem({
        titleId,
        copyId,
        payload,
        xFields,
    }: {
        titleId: string,
        copyId: string,
        payload: CopyReplace,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Copy_HATEOAS> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/titles/{titleId}/copies/{copyId}',
            path: {
                'titleId': titleId,
                'copyId': copyId,
            },
            headers: {
                'X-Fields': xFields,
            },
            body: payload,
        });
    }
    /**
     * Sửa một phần copy, theo ID
     * @returns Copy_HATEOAS Success
     * @throws ApiError
     */
    public static patchItem({
        titleId,
        copyId,
        payload,
        xFields,
    }: {
        titleId: string,
        copyId: string,
        payload: CopyUpdate,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Copy_HATEOAS> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/titles/{titleId}/copies/{copyId}',
            path: {
                'titleId': titleId,
                'copyId': copyId,
            },
            headers: {
                'X-Fields': xFields,
            },
            body: payload,
        });
    }
}
