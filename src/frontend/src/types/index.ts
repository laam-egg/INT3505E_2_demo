export interface Patron {
  id: string;
  name: string;
}

export interface PatronCreate {
  name: string;
}

export interface PatronUpdate {
  name?: string;
}

export interface Title {
  id: string;
  name: string;
  edition: number;
  authors: string; // newline-separated
  yearOfPublication: number;
  tags: string; // newline-separated
  totalCopies?: number;
  availableCopies?: number;
  borrowedCopies?: number;
  lostCopies?: number;
}

export interface TitleCreate {
  name: string;
  edition: number;
  authors: string;
  yearOfPublication: number;
  tags: string;
}

export interface TitleUpdate {
  name?: string;
  edition?: number;
  authors?: string;
  yearOfPublication?: number;
  tags?: string;
}

export interface Copy {
  id: string;
  titleId: string;
  code: string;
  status: 'AVAILABLE' | 'BORROWED' | 'LOST';
}

export interface CopyCreate {
  code: string;
}

export interface CopyUpdate {
  code?: string;
}

export interface Borrow {
  id: string;
  patronId: string;
  copyId: string;
  status: 'BORROWING' | 'RETURNED' | 'LOST';
  createdAt: string;
  statusLastUpdatedAt: string;
}

export interface BorrowCreate {
  patronId: string;
  copyId: string;
}

export interface BorrowUpdate {
  status: 'BORROWING' | 'RETURNED' | 'LOST';
}