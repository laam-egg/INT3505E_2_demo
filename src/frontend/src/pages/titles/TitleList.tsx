import { useState, useEffect } from 'react';
import { Table, Button, Space, message, Popconfirm, Tag } from 'antd';
import { Link } from 'react-router';
import { TitlesService, type Title } from '../../api';

export default function TitleListPage() {
  const [titles, setTitles] = useState<Title[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTitles();
  }, []);

  const fetchTitles = async () => {
    try {
      setLoading(true);
      const data = await TitlesService.getCollection({});
      setTitles(data.content || []);
    } catch (error) {
      message.error('Không thể tải danh sách đầu sách');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await TitlesService.deleteItem({ titleId: id });
      message.success('Xóa đầu sách thành công');
      fetchTitles();
    } catch (error) {
      message.error('Không thể xóa đầu sách');
    }
  };

  const columns = [
    {
      title: 'Tên sách',
      dataIndex: 'name',
      key: 'name',
      render: (text: string, record: Title) => (
        <span style={{ color: record.availableCopies === 0 ? '#999' : 'inherit' }}>
          {text}
        </span>
      ),
    },
    {
      title: 'Tái bản',
      dataIndex: 'edition',
      key: 'edition',
    },
    {
      title: 'Tác giả',
      dataIndex: 'authors',
      key: 'authors',
      render: (authors: string) => authors?.split('\\n').join(', '),
    },
    {
      title: 'Năm xuất bản',
      dataIndex: 'yearOfPublication',
      key: 'yearOfPublication',
    },
    {
      title: 'Thẻ',
      dataIndex: 'tags',
      key: 'tags',
      render: (tags: string) => (
        <>
          {tags?.split('\\n').map((tag, index) => (
            <Tag key={index} color="blue">{tag}</Tag>
          ))}
        </>
      ),
    },
    {
      title: 'Tổng số bản sao',
      dataIndex: 'totalCopies',
      key: 'totalCopies',
    },
    {
      title: 'Đang mượn',
      dataIndex: 'borrowedCopies',
      key: 'borrowedCopies',
    },
    {
      title: 'Có sẵn',
      dataIndex: 'availableCopies',
      key: 'availableCopies',
    },
    {
      title: 'Đã mất',
      dataIndex: 'lostCopies',
      key: 'lostCopies',
    },
    {
      title: 'Hành động',
      key: 'actions',
      render: (_: any, record: Title) => (
        <Space size="middle">
          <Link to={`/titles/${record.id}/copies`}>
            <Button type="link">Xem bản sao</Button>
          </Link>
          <Link to={`/titles/${record.id}`}>
            <Button type="primary">Chỉnh sửa</Button>
          </Link>
          <Popconfirm
            title="Bạn có chắc chắn muốn xóa đầu sách này?"
            onConfirm={() => record.id && handleDelete(record.id)}
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
        <h1>Danh sách đầu sách</h1>
        <Link to="/titles/create">
          <Button type="primary">Thêm đầu sách mới</Button>
        </Link>
      </div>
      <Table
        columns={columns}
        dataSource={titles}
        rowKey="id"
        loading={loading}
        pagination={{ pageSize: 10 }}
        scroll={{ x: true }}
      />
    </div>
  );
}