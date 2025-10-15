import { useState, useEffect } from 'react';
import { Descriptions, Button, message, Spin, Space, Tag } from 'antd';
import { useNavigate, useParams, Link } from 'react-router';
import { BorrowsService, type Borrow } from '../../api';

export default function BorrowUpdatePage() {
  const [_loading, setLoading] = useState(false);
  const [borrow, setBorrow] = useState<Borrow | null>(null);
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();

  useEffect(() => {
    if (id) {
      fetchBorrow(id);
    }
  }, [id]);

  const fetchBorrow = async (borrowId: string) => {
    try {
      setLoading(true);
      const data = await BorrowsService.getItem({ borrowId });
      setBorrow(data.content || null);
    } catch (error) {
      message.error('Không thể tải thông tin lượt mượn');
      navigate('/borrows');
    } finally {
      setLoading(false);
    }
  };

  const handleStatusUpdate = async (newStatus: string) => {
    if (!id) return;
    
    try {
      setLoading(true);
      await BorrowsService.patchItem({ 
        borrowId: id, 
        payload: { status: newStatus }
      });
      message.success('Cập nhật trạng thái thành công');
      navigate('/borrows');
    } catch (error) {
      message.error('Không thể cập nhật trạng thái');
    } finally {
      setLoading(false);
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

  const renderActionButtons = () => {
    if (!borrow) return null;

    const buttons = [];

    if (borrow.status === 'BORROWING') {
      buttons.push(
        <Button key="return" type="primary" onClick={() => handleStatusUpdate('RETURNED')}>
          Trả sách
        </Button>,
        <Button key="lost" danger onClick={() => handleStatusUpdate('LOST')}>
          Báo mất/hỏng sách
        </Button>
      );
    }

    if (borrow.status === 'RETURNED') {
      buttons.push(
        <Link key="reborrow" to={`/borrows/create?copyId=${borrow.copyId}`}>
          <Button type="primary">Cho mượn lại</Button>
        </Link>,
        <Button key="lost" danger onClick={() => handleStatusUpdate('LOST')}>
          Báo mất/hỏng sách
        </Button>
      );
    }

    if (borrow.status === 'LOST') {
      buttons.push(
        <Button key="return" type="primary" onClick={() => handleStatusUpdate('RETURNED')}>
          Trả/đền sách
        </Button>
      );
    }

    return <Space>{buttons}</Space>;
  };

  if (!borrow) {
    return <Spin size="large" style={{ display: 'block', textAlign: 'center', marginTop: 100 }} />;
  }

  return (
    <div>
      <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Thông tin lượt mượn sách</h1>
        <Button onClick={() => navigate('/borrows')}>Quay lại</Button>
      </div>
      
      <Descriptions bordered column={1} style={{ marginBottom: 16 }}>
        <Descriptions.Item label="ID lượt mượn">{borrow.id}</Descriptions.Item>
        <Descriptions.Item label="ID người mượn">{borrow.patronId}</Descriptions.Item>
        <Descriptions.Item label="ID sách">{borrow.copyId}</Descriptions.Item>
        <Descriptions.Item label="Trạng thái">
          <Tag color={getStatusColor(borrow.status)}>{getStatusText(borrow.status)}</Tag>
        </Descriptions.Item>
        <Descriptions.Item label="Ngày mượn">
          {borrow.createdAt ? new Date(borrow.createdAt).toLocaleString('vi-VN') : 'N/A'}
        </Descriptions.Item>
        <Descriptions.Item label="Cập nhật cuối">
          {borrow.statusLastUpdatedAt ? new Date(borrow.statusLastUpdatedAt).toLocaleString('vi-VN') : 'N/A'}
        </Descriptions.Item>
      </Descriptions>

      {renderActionButtons()}
    </div>
  );
}