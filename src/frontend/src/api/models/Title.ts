/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type Title = {
    /**
     * Tên đầu sách
     */
    name: string;
    /**
     * Số thứ tự của lần tái bản
     */
    edition: number;
    /**
     * Tên các tác giả, phân cách bằng newlines
     */
    authors: string;
    /**
     * Năm xuất bản
     */
    yearOfPublication: number;
    /**
     * Các thẻ/tags, phân cách bằng newlines
     */
    tags: string;
    /**
     * ID của đầu sách
     */
    readonly id?: string;
    /**
     * Tổng số bản sao của đầu sách này
     */
    readonly totalCopies?: number;
    /**
     * Số bản sao đang có sẵn (có thể mượn được)
     */
    readonly availableCopies?: number;
    /**
     * Số bản sao đang được mượn
     */
    readonly borrowedCopies?: number;
    /**
     * Số bản sao đã bị báo hỏng/mất
     */
    readonly lostCopies?: number;
};

