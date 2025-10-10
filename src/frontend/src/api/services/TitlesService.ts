/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Copy } from '../models/Copy';
import type { CopyCreate } from '../models/CopyCreate';
import type { CopyUpdate } from '../models/CopyUpdate';
import type { Title } from '../models/Title';
import type { TitleCreate } from '../models/TitleCreate';
import type { TitleUpdate } from '../models/TitleUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class TitlesService {
    /**
     * Create a new title
     * @returns Title Success
     * @throws ApiError
     */
    public static createANewTitle({
        payload,
        xFields,
    }: {
        payload: TitleCreate,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Title> {
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
     * Get all titles with pagination
     * @returns Title Success
     * @throws ApiError
     */
    public static getAllTitles({
        xFields,
    }: {
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Array<Title>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/titles/',
            headers: {
                'X-Fields': xFields,
            },
        });
    }
    /**
     * Update a title
     * @returns Title Success
     * @throws ApiError
     */
    public static updateTitleById({
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
    }): CancelablePromise<Title> {
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
    /**
     * Delete a title and all its copies
     * @returns any Success
     * @throws ApiError
     */
    public static deleteTitleById({
        titleId,
    }: {
        titleId: string,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/titles/{titleId}',
            path: {
                'titleId': titleId,
            },
        });
    }
    /**
     * Get a specific title by ID
     * @returns Title Success
     * @throws ApiError
     */
    public static getTitleById({
        titleId,
        xFields,
    }: {
        titleId: string,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Title> {
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
     * Create a new copy of a title
     * @returns Copy Success
     * @throws ApiError
     */
    public static createANewCopyOfATitle({
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
    }): CancelablePromise<Copy> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/titles/{titleId}/copies',
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
     * Get all copies of a specific title
     * @returns Copy Success
     * @throws ApiError
     */
    public static getAllCopiesOfATitle({
        titleId,
        xFields,
    }: {
        titleId: string,
        /**
         * An optional fields mask
         */
        xFields?: string,
    }): CancelablePromise<Array<Copy>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/titles/{titleId}/copies',
            path: {
                'titleId': titleId,
            },
            headers: {
                'X-Fields': xFields,
            },
        });
    }
    /**
     * Update a copy
     * @returns Copy Success
     * @throws ApiError
     */
    public static updateCopyById({
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
    }): CancelablePromise<Copy> {
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
    /**
     * Delete a copy
     * @returns any Success
     * @throws ApiError
     */
    public static deleteCopyById({
        titleId,
        copyId,
    }: {
        titleId: string,
        copyId: string,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/titles/{titleId}/copies/{copyId}',
            path: {
                'titleId': titleId,
                'copyId': copyId,
            },
        });
    }
    /**
     * Get a specific copy by ID
     * @returns Copy Success
     * @throws ApiError
     */
    public static getCopyById({
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
    }): CancelablePromise<Copy> {
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
}
