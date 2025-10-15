/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type Copy = {
    /**
     * Code/identifier của bản sao
     */
    code: string;
    /**
     * ID của bản sao
     */
    readonly id?: string;
    /**
     * ID của đầu sách tương ứng
     */
    titleId: string;
    /**
     * Trạng thái hiện tại của bản sao: AVAILABLE, BORROWED, or LOST
     */
    readonly status?: string;
};

