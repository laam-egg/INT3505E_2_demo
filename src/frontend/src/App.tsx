import { lazy, Suspense } from 'react';
import { BrowserRouter, Route, Routes, Link } from 'react-router';
import { Layout, Menu, Spin } from 'antd';
import { UserOutlined, BookOutlined, SwapOutlined } from '@ant-design/icons';

const { Header, Content, Sider } = Layout;

// Lazy load pages
const HomePage = lazy(() => import("./pages/home"));
const PatronListPage = lazy(() => import("./pages/patrons/PatronList"));
const PatronCreatePage = lazy(() => import("./pages/patrons/PatronCreate"));
const PatronUpdatePage = lazy(() => import("./pages/patrons/PatronUpdate"));
const TitleListPage = lazy(() => import("./pages/titles/TitleList"));
const TitleCreatePage = lazy(() => import("./pages/titles/TitleCreate"));
const TitleUpdatePage = lazy(() => import("./pages/titles/TitleUpdate"));
const CopyListPage = lazy(() => import("./pages/titles/CopyList"));
const CopyCreatePage = lazy(() => import("./pages/titles/CopyCreate"));
const CopyUpdatePage = lazy(() => import("./pages/titles/CopyUpdate"));
const BorrowListPage = lazy(() => import("./pages/borrows/BorrowList"));
const BorrowCreatePage = lazy(() => import("./pages/borrows/BorrowCreate"));
const BorrowUpdatePage = lazy(() => import("./pages/borrows/BorrowUpdate"));

const menuItems = [
  {
    key: 'home',
    icon: <UserOutlined />,
    label: <Link to="/">Trang chủ</Link>,
  },
  {
    key: 'patrons',
    icon: <UserOutlined />,
    label: 'Người dùng',
    children: [
      {
        key: 'patrons-list',
        label: <Link to="/patrons">Danh sách người dùng</Link>,
      },
      {
        key: 'patrons-create',
        label: <Link to="/patrons/create">Thêm người dùng</Link>,
      },
    ],
  },
  {
    key: 'titles',
    icon: <BookOutlined />,
    label: 'Đầu sách',
    children: [
      {
        key: 'titles-list',
        label: <Link to="/titles">Danh sách đầu sách</Link>,
      },
      {
        key: 'titles-create',
        label: <Link to="/titles/create">Thêm đầu sách</Link>,
      },
    ],
  },
  {
    key: 'borrows',
    icon: <SwapOutlined />,
    label: 'Mượn sách',
    children: [
      {
        key: 'borrows-list',
        label: <Link to="/borrows">Danh sách mượn sách</Link>,
      },
      {
        key: 'borrows-create',
        label: <Link to="/borrows/create">Cho mượn sách</Link>,
      },
    ],
  },
];

function App() {
  return (
    <BrowserRouter>
      <Layout style={{ minHeight: '100vh' }}>
        <Sider width={250} theme="light">
          <div style={{ padding: '16px', textAlign: 'center', fontWeight: 'bold' }}>
            Hệ thống thư viện
          </div>
          <Menu
            mode="inline"
            defaultSelectedKeys={['home']}
            defaultOpenKeys={['patrons', 'titles', 'borrows']}
            items={menuItems}
          />
        </Sider>
        <Layout>
          <Header style={{ padding: 0, background: '#fff', paddingLeft: 24 }}>
            <h1 style={{ margin: 0, fontSize: '18px' }}>Hệ thống quản lý thư viện</h1>
          </Header>
          <Content style={{ margin: '16px', padding: 24, background: '#fff' }}>
            <Suspense fallback={<Spin size="large" style={{ display: 'block', textAlign: 'center', marginTop: 100 }} />}>
              <Routes>
                <Route path="/" element={<HomePage />} />
                
                {/* Patron routes */}
                <Route path="/patrons" element={<PatronListPage />} />
                <Route path="/patrons/create" element={<PatronCreatePage />} />
                <Route path="/patrons/:id" element={<PatronUpdatePage />} />
                
                {/* Title routes */}
                <Route path="/titles" element={<TitleListPage />} />
                <Route path="/titles/create" element={<TitleCreatePage />} />
                <Route path="/titles/:id" element={<TitleUpdatePage />} />
                
                {/* Copy routes */}
                <Route path="/titles/:titleId/copies" element={<CopyListPage />} />
                <Route path="/titles/:titleId/copies/create" element={<CopyCreatePage />} />
                <Route path="/titles/:titleId/copies/:copyId" element={<CopyUpdatePage />} />
                
                {/* Borrow routes */}
                <Route path="/borrows" element={<BorrowListPage />} />
                <Route path="/borrows/create" element={<BorrowCreatePage />} />
                <Route path="/borrows/:id" element={<BorrowUpdatePage />} />
              </Routes>
            </Suspense>
          </Content>
        </Layout>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
