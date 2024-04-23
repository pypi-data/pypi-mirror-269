//! Implementation of the ``rust:variable::`` directive

use quote::quote;
use syn::{Fields, ImplItemConst, ItemConst, ItemStatic, TraitItemConst, Visibility};

use crate::check_visibility;
use crate::directives::{extract_doc_from_attrs, Directive, DirectiveOption, DirectiveVisibility};
use crate::formats::{MdContent, MdDirective, RstContent, RstDirective};

#[derive(Clone, Debug)]
pub(crate) struct VariableDirective {
    pub(crate) name: String,
    pub(crate) options: Vec<DirectiveOption>,
    pub(crate) content: Vec<String>,
}

macro_rules! var_from_item {
    ($item:expr, $ty:expr, $parent_path:expr, $vis:expr, $inherited:expr, $prefix:expr) => {{
        let name = format!("{}::{}", $parent_path, &$item.ident);
        let ty = $ty;
        let options = vec![
            DirectiveOption::Vis(DirectiveVisibility::effective_visibility(&$vis, $inherited)),
            DirectiveOption::Sig(format!("{}{}: {}", $prefix, &$item.ident, quote! {#ty})),
            DirectiveOption::Type(quote! {#ty}.to_string()),
            DirectiveOption::Toc(format!("{}{}", $prefix, &$item.ident)),
        ];

        Directive::Variable(VariableDirective {
            name,
            options,
            content: extract_doc_from_attrs(&$item.attrs),
        })
    }};
}

impl VariableDirective {
    pub(crate) fn from_fields(
        parent_path: &str,
        fields: &Fields,
        inherited_visibility: &Option<&Visibility>,
    ) -> Vec<VariableDirective> {
        if let Fields::Named(named_fields) = fields {
            named_fields
                .named
                .iter()
                .map(|f| {
                    let ty = &f.ty;
                    let options = vec![
                        DirectiveOption::Vis(DirectiveVisibility::effective_visibility(
                            &f.vis,
                            inherited_visibility,
                        )),
                        DirectiveOption::Sig(format!(
                            "{}: {}",
                            f.ident.as_ref().unwrap(),
                            quote! {#ty}
                        )),
                        DirectiveOption::Type(quote! {#ty}.to_string()),
                        DirectiveOption::Toc(format!("{}", f.ident.as_ref().unwrap())),
                    ];

                    VariableDirective {
                        name: format!("{}::{}", parent_path, f.ident.as_ref().unwrap()),
                        options,
                        content: extract_doc_from_attrs(&f.attrs),
                    }
                })
                .collect()
        }
        else {
            Vec::new()
        }
    }

    pub(crate) fn from_static(
        parent_path: &str,
        item: &ItemStatic,
        inherited_visibility: &Option<&Visibility>,
    ) -> Directive {
        var_from_item!(
            item,
            item.ty.as_ref(),
            parent_path,
            item.vis,
            inherited_visibility,
            "static "
        )
    }

    pub(crate) fn from_const(
        parent_path: &str,
        item: &ItemConst,
        inherited_visibility: &Option<&Visibility>,
    ) -> Directive {
        var_from_item!(
            item,
            item.ty.as_ref(),
            parent_path,
            item.vis,
            inherited_visibility,
            "const "
        )
    }

    pub(crate) fn from_impl_const(
        parent_path: &str,
        item: &ImplItemConst,
        inherited_visibility: &Option<&Visibility>,
    ) -> Directive {
        var_from_item!(
            item,
            &item.ty,
            parent_path,
            item.vis,
            inherited_visibility,
            "const "
        )
    }

    pub(crate) fn from_trait_const(
        parent_path: &str,
        item: &TraitItemConst,
        inherited_visibility: &Option<&Visibility>,
    ) -> Directive {
        var_from_item!(
            item,
            &item.ty,
            parent_path,
            Visibility::Inherited,
            inherited_visibility,
            "const "
        )
    }
}

impl RstDirective for VariableDirective {
    fn get_rst_text(self, level: usize, max_visibility: &DirectiveVisibility) -> Vec<String> {
        check_visibility!(self.options, max_visibility);
        let content_indent = Self::make_indent(level + 1);

        let mut text = Self::make_rst_header("variable", &self.name, &self.options, level);
        text.extend(self.content.get_rst_text(&content_indent));

        text
    }
}

impl MdDirective for VariableDirective {
    fn get_md_text(self, fence_size: usize, max_visibility: &DirectiveVisibility) -> Vec<String> {
        check_visibility!(self.options, max_visibility);
        let fence = Self::make_fence(fence_size);

        let mut text = Self::make_md_header("variable", &self.name, &self.options, &fence);
        text.extend(self.content.get_md_text());

        text.push(fence);
        text
    }
}
