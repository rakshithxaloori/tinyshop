interface TemplateBuilderProps {
  template: Template;
  onChange: (template: Template) => void;
  onRemove: () => void;
}

const TemplateBuilder = (props: TemplateBuilderProps) => {
  const { template } = props;
  return (
    <div>
      <h1>Template Builder</h1>
    </div>
  );
}