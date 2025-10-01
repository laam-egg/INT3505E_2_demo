import { useState } from 'react';
import { Form, Input, InputNumber, Button, message } from 'antd';
import { useNavigate } from 'react-router';
import { TitlesService, type TitleCreate } from '../../api';

const { TextArea } = Input;

export default function TitleCreatePage() {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (values: any) => {
    try {
      setLoading(true);
      
      // Convert authors and tags arrays to newline-separated strings
      const payload: TitleCreate = {
        name: values.name,
        edition: values.edition,
        authors: values.authors?.split('\n').filter((a: string) => a.trim()).join('\n') || '',
        yearOfPublication: values.yearOfPublication,
        tags: values.tags?.split('\n').filter((t: string) => t.trim()).join('\n') || ''
      };

      await TitlesService.createANewTitle({ payload });
      message.success('Thêm đầu sách thành công');
      navigate('/titles');
    } catch (error) {
      message.error('Không thể thêm đầu sách');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Thêm đầu sách mới</h1>
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
            Thêm
          </Button>
          <Button style={{ marginLeft: 8 }} onClick={() => navigate('/titles')}>
            Hủy
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}