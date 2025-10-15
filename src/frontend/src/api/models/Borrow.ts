/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type Borrow = {
    /**
     * ID người mượn (patron)
     */
    patronId: string;
    /**
     * ID bản sao của một sách nào đó được mượn
     */
    copyId: string;
    /**
     * ID lượt mượn
     */
    readonly id?: string;
    /**
     * Trạng thái của lượt mượn: BORROWING, RETURNED, or LOST
     */
    status: string;
    /**
     * Thời gian mượn (tức thời gian tạo lượt mượn)
     */
    readonly createdAt?: string;
    /**
     * Thời gian cuối cùng trạng thái của lượt mượn này được cập nhật
     */
    readonly statusLastUpdatedAt?: string;
};

