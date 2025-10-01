import { useState, useEffect } from 'react';
import { Form, Input, InputNumber, Button, message, Spin } from 'antd';
import { useNavigate, useParams } from 'react-router';
import { TitlesService, type Title, type TitleUpdate } from '../../api';

const { TextArea } = Input;

export default function TitleUpdatePage() {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [title, setTitle] = useState<Title | null>(null);
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();

  useEffect(() => {
    if (id) {
      fetchTitle(id);
    }
  }, [id]);

  const fetchTitle = async (titleId: string) => {
    try {
      setLoading(true);
      const data = await TitlesService.getTitleById({ titleId });
      setTitle(data);
      
      // Set form values, converting newline-separated strings back to form format
      form.setFieldsValue({
        ...data,
        authors: data.authors?.split('\n').join('\n'),
        tags: data.tags?.split('\n').join('\n')
      });
    } catch (error) {
      message.error('Không thể tải thông tin đầu sách');
      navigate('/titles');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (values: any) => {
    if (!id) return;

    try {
      setLoading(true);
      
      // Convert authors and tags arrays to newline-separated strings
      const payload: TitleUpdate = {
        name: values.name,
        edition: values.edition,
        authors: values.authors?.split('\n').filter((a: string) => a.trim()).join('\n') || '',
        yearOfPublication: values.yearOfPublication,
        tags: values.tags?.split('\n').filter((t: string) => t.trim()).join('\n') || ''
      };

      await TitlesService.updateTitleById({ titleId: id, payload });
      message.success('Cập nhật đầu sách thành công');
      navigate('/titles');
    } catch (error) {
      message.error('Không thể cập nhật đầu sách');
    } finally {
      setLoading(false);
    }
  };

  if (!title) {
    return <Spin size="large" style={{ display: 'block', textAlign: 'center', marginTop: 100 }} />;
  }

  return (
    <div>
      <h1>Chỉnh sửa đầu sách</h1>
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        style={{ maxWidth: 600 }}
      >
        <Form.Item
          name="name"
          label="Tên đầu sách"
          rules={[{ required: true, message: 'Vui lòng nhập tên đầu sách' }]}
        >
          <Input placeholder="Nhập tên đầu sách" />
        </Form.Item>

        <Form.Item
          name="edition"
          label="Tái bản"
          rules={[{ required: true, message: 'Vui lòng nhập số tái bản' }]}
        >
          <InputNumber min={1} placeholder="Nhập số tái bản" style={{ width: '100%' }} />
        </Form.Item>

        <Form.Item
          name="authors"
          label="Tác giả"
          rules={[{ required: true, message: 'Vui lòng nhập tác giả' }]}
          extra="Mỗi tác giả trên một dòng"
        >
          <TextArea 
            rows={4} 
            placeholder="Nhập tên các tác giả, mỗi tác giả trên một dòng"
          />
        </Form.Item>

        <Form.Item
          name="yearOfPublication"
          label="Năm xuất bản"
          rules={[{ required: true, message: 'Vui lòng nhập năm xuất bản' }]}
        >
          <InputNumber min={1000} max={new Date().getFullYear() + 10} placeholder="Nhập năm xuất bản" style={{ width: '100%' }} />
        </Form.Item>

        <Form.Item
          name="tags"
          label="Thẻ phân loại"
          extra="Mỗi thẻ trên một dòng"
        >
          <TextArea 
            rows={3} 
            placeholder="Nhập các thẻ phân loại, mỗi thẻ trên một dòng"
          />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading}>
            Cập nhật
          </Button>
          <Button style={{ marginLeft: 8 }} onClick={() => navigate('/titles')}>
            Hủy
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}