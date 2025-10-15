/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { empty_HATEOAS } from '../models/empty_HATEOAS';
import type { Title_HATEOAS } from '../models/Title_HATEOAS';
import type { TitleCreate } from '../models/TitleCreate';
import type { TitleList_HATEOAS } from '../models/TitleList_HATEOAS';
import type { TitleReplace } from '../models/TitleReplace';
import type { TitleUpdate } from '../models/TitleUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class TitlesService {
    /**
     * Lấy danh sách tất cả các titles, có pagination.
     * @returns TitleList_HATEOAS Success
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
    }): CancelablePromise<TitleList_HATEOAS> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/titles/',
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
     * Thêm đầu sách mới.
     * @returns Title_HATEOAS Success
     * @throws ApiError
     */
    public static postCollection({
        payload,
        xFields,
    }: {
        payload: TitleCreate,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Title_HATEOAS> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/titles/',
            headers: {
                'X-Fields': xFields,
            },
            body: payload,
        });
    }
    /**
     * Xóa title, theo ID
     * @returns empty_HATEOAS Success
     * @throws ApiError
     */
    public static deleteItem({
        titleId,
        xFields,
    }: {
        titleId: string,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<empty_HATEOAS> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/titles/{titleId}',
            path: {
                'titleId': titleId,
            },
            headers: {
                'X-Fields': xFields,
            },
        });
    }
    /**
     * Lấy title theo ID
     * @returns Title_HATEOAS Success
     * @throws ApiError
     */
    public static getItem({
        titleId,
        xFields,
    }: {
        titleId: string,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Title_HATEOAS> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/titles/{titleId}',
            path: {
                'titleId': titleId,
            },
            headers: {
                'X-Fields': xFields,
            },
        });
    }
    /**
     * Sửa toàn bộ title, theo ID
     * @returns Title_HATEOAS Success
     * @throws ApiError
     */
    public static putItem({
        titleId,
        payload,
        xFields,
    }: {
        titleId: string,
        payload: TitleReplace,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Title_HATEOAS> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/titles/{titleId}',
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
     * Sửa một phần title, theo ID
     * @returns Title_HATEOAS Success
     * @throws ApiError
     */
    public static patchItem({
        titleId,
        payload,
        xFields,
    }: {
        titleId: string,
        payload: TitleUpdate,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Title_HATEOAS> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/titles/{titleId}',
            path: {
                'titleId': titleId,
            },
            headers: {
                'X-Fields': xFields,
            },
            body: payload,
        });
    }
}
