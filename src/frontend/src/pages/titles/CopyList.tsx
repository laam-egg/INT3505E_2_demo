import { useState, useEffect } from 'react';
import { Table, Button, Space, message, Popconfirm, Tag } from 'antd';
import { Link, useParams } from 'react-router';
import { TitlesService, type Copy } from '../../api';

export default function CopyListPage() {
  const [copies, setCopies] = useState<Copy[]>([]);
  const [loading, setLoading] = useState(true);
  const { titleId } = useParams<{ titleId: string }>();

  useEffect(() => {
    if (titleId) {
      fetchCopies();
    }
  }, [titleId]);

  const fetchCopies = async () => {
    if (!titleId) return;
    try {
      setLoading(true);
      const data = await TitlesService.getAllCopiesOfATitle({ titleId });
      setCopies(data || []);
    } catch (error) {
      message.error('Không thể tải danh sách bản sao');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (copyId: string) => {
    if (!titleId) return;
    try {
      await TitlesService.deleteCopyById({ titleId, copyId });
      message.success('Xóa bản sao thành công');
      fetchCopies();
    } catch (error) {
      message.error('Không thể xóa bản sao');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'AVAILABLE': return 'green';
      case 'BORROWED': return 'orange';
      case 'LOST': return 'red';
      default: return 'default';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'AVAILABLE': return 'Có sẵn';
      case 'BORROWED': return 'Đang được mượn';
      case 'LOST': return 'Đã mất';
      default: return status;
    }
  };

  const columns = [
    {
      title: 'Mã sách',
      dataIndex: 'code',
      key: 'code',
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
      title: 'Hành động',
      key: 'actions',
      render: (_: any, record: Copy) => (
        <Space size="middle">
          {record.status === 'AVAILABLE' && (
            <Link to={`/borrows/create?titleId=${titleId}&copyId=${record.id}`}>
              <Button type="primary">Cho mượn</Button>
            </Link>
          )}
          {record.status !== 'AVAILABLE' && (
            <Button type="link">Xem lượt mượn</Button>
          )}
          <Link to={`/titles/${titleId}/copies/${record.id}`}>
            <Button>Sửa</Button>
          </Link>
          <Popconfirm
            title="Bạn có chắc chắn muốn xóa bản sao này?"
            onConfirm={() => handleDelete(record.id!)}
            okText="Có"
            cancelText="Không"
          >
            <Button danger>Xóa</Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Danh sách bản sao</h1>
        <Space>
          <Link to={`/titles/${titleId}/copies/create`}>
            <Button type="primary">Thêm bản sao mới</Button>
          </Link>
          <Link to="/titles">
            <Button>Quay lại danh sách đầu sách</Button>
          </Link>
        </Space>
      </div>
      <Table
        columns={columns}
        dataSource={copies}
        rowKey="id"
        loading={loading}
        pagination={{ pageSize: 10 }}
      />
    </div>
  );
}