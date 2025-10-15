import { useState, useEffect } from 'react';
import { Table, Button, Space, message, Select, Tag } from 'antd';
import { Link, useSearchParams } from 'react-router';
import { BorrowsService, PatronsService, type Borrow, type Patron } from '../../api';

const { Option } = Select;

export default function BorrowListPage() {
  const [borrows, setBorrows] = useState<Borrow[]>([]);
  const [patrons, setPatrons] = useState<Patron[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedPatronId, setSelectedPatronId] = useState<string | null>(null);
  const [_selectedCopyId, setSelectedCopyId] = useState<string | null>(null);
  const [searchParams, setSearchParams] = useSearchParams();

  useEffect(() => {
    fetchPatrons();
    
    // Get patronId from URL params
    const patronId = searchParams.get('patronId') || null;
    setSelectedPatronId(patronId);

    // TODO: A dropdown to select copy as well.
    // Get copyId from URL params
    const copyId = searchParams.get('copyId') || null;
    setSelectedCopyId(copyId);
    
    fetchBorrows();
  }, [searchParams]);

  const fetchPatrons = async () => {
    try {
      const data = await PatronsService.getCollection({});
      setPatrons(data.content || []);
    } catch (error) {
      console.error('Failed to fetch patrons');
    }
  };

  const fetchBorrows = async () => {
    try {
      setLoading(true);
      const patronId = searchParams.get('patronId') || undefined;
      const copyId = searchParams.get('copyId') || undefined;
      
      const data = await BorrowsService.getCollection({
        patronId, copyId,

        ...(copyId ? {
          pageNumber: 0,
          pageSize: 1,
        } : {}),
      });

      setBorrows(data.content || []);
    } catch (error) {
      message.error('Không thể tải danh sách mượn sách');
    } finally {
      setLoading(false);
    }
  };

  const handlePatronChange = (patronId: string | null | undefined) => {
    patronId = patronId || null;
    setSelectedPatronId(patronId);
    const newParams = new URLSearchParams(searchParams);
    if (patronId) {
      newParams.set('patronId', patronId);
    } else {
      newParams.delete('patronId');
    }
    setSearchParams(newParams);
  };

  const handleStatusUpdate = async (borrowId: string, newStatus: string) => {
    try {
      await BorrowsService.patchItem({ 
        borrowId, 
        payload: { status: newStatus as any }
      });
      message.success('Cập nhật trạng thái thành công');
      fetchBorrows();
    } catch (error) {
      message.error('Không thể cập nhật trạng thái');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'BORROWING': return 'blue';
      case 'RETURNED': return 'green';
      case 'LOST': return 'red';
      default: return 'default';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'BORROWING': return 'Đang mượn';
      case 'RETURNED': return 'Đã trả';
      case 'LOST': return 'Đã mất/hỏng';
      default: return status;
    }
  };

  const renderActionButtons = (record: Borrow) => {
    const buttons = [
      <Link key="detail" to={`/borrows/${record.id}`}>
        <Button type="link">Xem chi tiết</Button>
      </Link>
    ];

    if (record.status === 'BORROWING') {
      buttons.push(
        <Button key="return" onClick={() => handleStatusUpdate(record.id!, 'RETURNED')}>
          Trả sách
        </Button>,
        <Button key="lost" danger onClick={() => handleStatusUpdate(record.id!, 'LOST')}>
          Báo mất/hỏng sách
        </Button>
      );
    }

    if (record.status === 'RETURNED') {
      buttons.push(
        <Link key="reborrow" to={`/borrows/create?copyId=${record.copyId}`}>
          <Button type="primary">Cho mượn lại</Button>
        </Link>,
        <Button key="lost" danger onClick={() => handleStatusUpdate(record.id!, 'LOST')}>
          Báo mất/hỏng sách
        </Button>
      );
    }

    if (record.status === 'LOST') {
      buttons.push(
        <Button key="return" type="primary" onClick={() => handleStatusUpdate(record.id!, 'RETURNED')}>
          Trả/đền sách
        </Button>
      );
    }

    return <Space size="small">{buttons}</Space>;
  };

  const columns = [
    {
      title: 'ID người mượn',
      dataIndex: 'patronId',
      key: 'patronId',
    },
    {
      title: 'ID sách',
      dataIndex: 'copyId',
      key: 'copyId',
    },
    {
      title: 'Trạng thái',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={getStatusColor(status)}>{getStatusText(status)}</Tag>
      ),
    },
    {
      title: 'Ngày mượn',
      dataIndex: 'createdAt',
      key: 'createdAt',
      render: (date: string) => new Date(date).toLocaleString('vi-VN'),
    },
    {
      title: 'Cập nhật cuối',
      dataIndex: 'statusLastUpdatedAt',
      key: 'statusLastUpdatedAt',
      render: (date: string) => new Date(date).toLocaleString('vi-VN'),
    },
    {
      title: 'Hành động',
      key: 'actions',
      render: (_: any, record: Borrow) => renderActionButtons(record),
    },
  ];

  return (
    <div>
      <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Danh sách mượn sách</h1>
        <Link to="/borrows/create">
          <Button type="primary">Cho mượn sách</Button>
        </Link>
      </div>
      
      <div style={{ marginBottom: 16 }}>
        <label>Lọc theo người dùng: </label>
        <Select
          style={{ width: 300 }}
          placeholder="Chọn người dùng"
          value={selectedPatronId}
          onChange={handlePatronChange}
          allowClear
        >
          {patrons.map(patron => (
            <Option key={patron.id} value={patron.id!}>{patron.name}</Option>
          ))}
        </Select>
      </div>

      <Table
        columns={columns}
        dataSource={borrows}
        rowKey="id"
        loading={loading}
        pagination={{ pageSize: 10 }}
        scroll={{ x: true }}
      />
    </div>
  );
}