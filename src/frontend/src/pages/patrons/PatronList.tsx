import { useState, useEffect } from 'react';
import { Table, Button, Space, message, Popconfirm } from 'antd';
import { Link } from 'react-router';
import { PatronsService, type Patron } from '../../api';

export default function PatronListPage() {
  const [patrons, setPatrons] = useState<Patron[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPatrons();
  }, []);

  const fetchPatrons = async () => {
    try {
      setLoading(true);
      const data = await PatronsService.getAllPatrons({});
      setPatrons(data || []);
    } catch (error) {
      message.error('Không thể tải danh sách người dùng');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await PatronsService.deletePatronById({ patronId: id });
      message.success('Xóa người dùng thành công');
      fetchPatrons();
    } catch (error) {
      message.error('Không thể xóa người dùng');
    }
  };

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
    },
    {
      title: 'Tên',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Hành động',
      key: 'actions',
      render: (_: any, record: any) => (
        <Space size="middle">
          <Link to={`/borrows?patronId=${record.id}`}>
            <Button type="link">Xem tình trạng mượn sách</Button>
          </Link>
          <Link to={`/patrons/${record.id}`}>
            <Button type="primary">Chỉnh sửa</Button>
          </Link>
          <Popconfirm
            title="Bạn có chắc chắn muốn xóa người dùng này?"
            onConfirm={() => handleDelete(record.id)}
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
        <h1>Danh sách người dùng</h1>
        <Link to="/patrons/create">
          <Button type="primary">Thêm người dùng mới</Button>
        </Link>
      </div>
      <Table
        columns={columns}
        dataSource={patrons}
        rowKey="id"
        loading={loading}
        pagination={{ pageSize: 10 }}
      />
    </div>
  );
}