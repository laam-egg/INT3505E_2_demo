/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type Title = {
    /**
     * Newline-separated list of authors
     */
    authors: string;
    /**
     * Number of available copies
     */
    readonly availableCopies?: number;
    /**
     * Number of borrowed copies
     */
    readonly borrowedCopies?: number;
    /**
     * Edition number
     */
    edition: number;
    /**
     * The title ID
     */
    readonly id?: string;
    /**
     * Number of lost copies
     */
    readonly lostCopies?: number;
    /**
     * Title name
     */
    name: string;
    /**
     * Newline-separated list of tags
     */
    tags: string;
    /**
     * Total number of copies
     */
    readonly totalCopies?: number;
    /**
     * Year of publication
     */
    yearOfPublication: number;
};

